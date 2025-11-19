"""Excel file importer for RS.ge data."""
from typing import Dict, List, Optional
import pandas as pd
from tax_core.importers.base_importer import BaseImporter, ImportResult
from tax_core.models import (
    UserProfile,
    ResidencyStatus,
    SalaryIncome,
    MicroBusinessIncome,
    SmallBusinessIncome,
    RentalIncome,
    CapitalGainsIncome,
    DividendsIncome,
    InterestIncome,
    PropertyTaxInput,
)


class ExcelImporter(BaseImporter):
    """Import Excel files exported from RS.ge."""
    
    # Expected sheet names (flexible matching)
    EXPECTED_SHEETS = {
        "income": ["income", "declarations", "revenue", "earnings"],
        "property": ["property", "properties", "real estate"],
        "payments": ["payments", "tax payments", "history"],
    }
    
    def parse(self, file_path: str) -> Dict:
        """
        Parse Excel file.
        
        Args:
            file_path: Path to Excel file or file-like object
            
        Returns:
            Dict: Parsed Excel data
        """
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                # Convert to list of dictionaries
                sheets_data[sheet_name] = df.to_dict('records')
            
            return {
                "sheets": sheets_data,
                "sheet_names": excel_file.sheet_names,
            }
        except Exception as e:
            raise ValueError(f"Failed to parse Excel file: {str(e)}")
    
    def validate(self, data: Dict) -> bool:
        """
        Validate Excel data structure.
        
        Args:
            data: Parsed Excel data
            
        Returns:
            bool: True if valid
        """
        if "sheets" not in data or not data["sheets"]:
            self.errors.append("Excel file has no sheets")
            return False
        
        # Check if we have at least one sheet with data
        has_data = False
        for sheet_name, rows in data["sheets"].items():
            if rows:
                has_data = True
                break
        
        if not has_data:
            self.errors.append("Excel file has no data")
            return False
        
        return True
    
    def extract_user_profile(self, data: Dict, year: int) -> UserProfile:
        """
        Extract UserProfile from Excel data.
        
        Args:
            data: Parsed Excel data
            year: Tax year
            
        Returns:
            UserProfile: Extracted user profile
        """
        sheets = data["sheets"]
        
        # Find income sheet
        income_sheet = self._find_sheet(sheets, self.EXPECTED_SHEETS["income"])
        if not income_sheet:
            # Use first sheet as fallback
            income_sheet = list(sheets.values())[0] if sheets else []
        
        # Find property sheet
        property_sheet = self._find_sheet(sheets, self.EXPECTED_SHEETS["property"])
        
        # Initialize income lists
        salary = []
        micro_business = []
        small_business = []
        rental = []
        capital_gains = []
        dividends = []
        interest = []
        property_values = []
        property_types = []
        family_income = 0.0
        
        # Process income sheet
        for row in income_sheet:
            try:
                # Convert row to dict if it's a Series
                if hasattr(row, 'to_dict'):
                    row = row.to_dict()
                
                # Get income type (try different column names)
                income_type = str(self._get_value(row, ["income_type", "type", "category", "income category"], "")).lower()
                amount = self._parse_float(self._get_value(row, ["amount", "value", "income", "revenue"], "0"))
                
                if amount <= 0:
                    continue
                
                # Map income types (similar to CSV importer)
                if "salary" in income_type or "employment" in income_type or "wage" in income_type:
                    months = self._parse_int(self._get_value(row, ["months", "month_count"], "12"))
                    salary.append(SalaryIncome(
                        monthly_gross=amount / months if months > 0 else amount / 12,
                        months=months if months > 0 else 12,
                    ))
                    family_income += amount
                
                elif "micro" in income_type and "business" in income_type:
                    micro_business.append(MicroBusinessIncome(
                        turnover=amount,
                    ))
                    family_income += amount
                
                elif "small" in income_type and "business" in income_type:
                    small_business.append(SmallBusinessIncome(
                        turnover=amount,
                    ))
                    family_income += amount
                
                elif "rental" in income_type or "rent" in income_type:
                    months = self._parse_int(self._get_value(row, ["months", "month_count"], "12"))
                    monthly_rent = amount / months if months > 0 else amount / 12
                    rental.append(RentalIncome(
                        monthly_rent=monthly_rent,
                        months=months if months > 0 else 12,
                    ))
                    family_income += amount
                
                elif "capital" in income_type and "gain" in income_type:
                    purchase_price = self._parse_float(self._get_value(row, ["purchase_price", "purchase"], "0"))
                    sale_price = self._parse_float(self._get_value(row, ["sale_price", "sale"], str(amount)))
                    if purchase_price == 0:
                        purchase_price = sale_price - amount
                    capital_gains.append(CapitalGainsIncome(
                        purchase_price=purchase_price,
                        sale_price=sale_price,
                    ))
                    family_income += max(0, sale_price - purchase_price)
                
                elif "dividend" in income_type:
                    dividends.append(DividendsIncome(amount=amount))
                    family_income += amount
                
                elif "interest" in income_type:
                    interest.append(InterestIncome(amount=amount))
                    family_income += amount
            
            except Exception as e:
                self.warnings.append(f"Skipped row due to error: {str(e)}")
                continue
        
        # Process property sheet
        if property_sheet:
            for row in property_sheet:
                try:
                    if hasattr(row, 'to_dict'):
                        row = row.to_dict()
                    
                    property_value = self._parse_float(self._get_value(row, ["value", "assessed_value", "market_value", "amount"], "0"))
                    if property_value > 0:
                        property_values.append(property_value)
                        property_type = str(self._get_value(row, ["type", "property_type"], "residential")).lower()
                        property_types.append(property_type)
                
                except Exception as e:
                    self.warnings.append(f"Skipped property row due to error: {str(e)}")
                    continue
        
        # Create property tax input if properties found
        property_tax = []
        if property_values:
            property_tax.append(PropertyTaxInput(
                family_income=family_income,
                properties=len(property_values),
                property_values=property_values,
                property_types=property_types,
            ))
        
        return UserProfile(
            year=year,
            residency=ResidencyStatus.RESIDENT,
            family_income=family_income,
            salary=salary,
            micro_business=micro_business,
            small_business=small_business,
            rental=rental,
            capital_gains=capital_gains,
            dividends=dividends,
            interest=interest,
            property_tax=property_tax,
        )
    
    def _find_sheet(self, sheets: Dict, possible_names: List[str]) -> Optional[List]:
        """Find sheet by name (case-insensitive)."""
        for sheet_name, data in sheets.items():
            if any(name.lower() in sheet_name.lower() for name in possible_names):
                return data
        return None
    
    def _get_value(self, row: Dict, possible_keys: List[str], default: str = "") -> str:
        """Get value from row using possible key names."""
        for key in possible_keys:
            for k, v in row.items():
                if str(k).lower() == key.lower():
                    return str(v) if pd.notna(v) else default
        return default
    
    def _parse_float(self, value: str) -> float:
        """Parse float value, handling commas and spaces."""
        if not value or pd.isna(value):
            return 0.0
        cleaned = str(value).replace(",", "").replace(" ", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def _parse_int(self, value: str) -> int:
        """Parse integer value."""
        if not value or pd.isna(value):
            return 0
        try:
            return int(float(str(value).replace(",", "").strip()))
        except ValueError:
            return 0

