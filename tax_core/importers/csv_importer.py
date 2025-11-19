"""CSV file importer for RS.ge data."""
import csv
import io
from typing import Dict, List, Optional
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


class CSVImporter(BaseImporter):
    """Import CSV files exported from RS.ge."""
    
    # Expected CSV column names (flexible matching)
    EXPECTED_COLUMNS = {
        "income_type": ["income_type", "type", "income category", "category"],
        "amount": ["amount", "value", "income", "revenue"],
        "period": ["period", "time_period", "frequency"],
        "year": ["year", "tax_year", "fiscal_year"],
        "months": ["months", "month_count"],
        "description": ["description", "notes", "details"],
    }
    
    def parse(self, file_path: str) -> Dict:
        """
        Parse CSV file.
        
        Args:
            file_path: Path to CSV file or file-like object
            
        Returns:
            Dict: Parsed CSV data
        """
        # Handle file path or file-like object
        if isinstance(file_path, str):
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return self._parse_csv_file(f)
        else:
            # File-like object (e.g., from Streamlit upload)
            return self._parse_csv_file(file_path)
    
    def _parse_csv_file(self, file_obj) -> Dict:
        """Parse CSV file object."""
        # Try to detect delimiter
        sample = file_obj.read(1024)
        file_obj.seek(0)
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        rows = list(reader)
        
        if not rows:
            raise ValueError("CSV file is empty or has no data rows")
        
        return {
            "rows": rows,
            "headers": reader.fieldnames or [],
        }
    
    def validate(self, data: Dict) -> bool:
        """
        Validate CSV data structure.
        
        Args:
            data: Parsed CSV data
            
        Returns:
            bool: True if valid
        """
        if "rows" not in data or not data["rows"]:
            self.errors.append("CSV file has no data rows")
            return False
        
        headers = data.get("headers", [])
        if not headers:
            self.errors.append("CSV file has no headers")
            return False
        
        # Check for required columns (flexible matching)
        required_found = {}
        for key, possible_names in self.EXPECTED_COLUMNS.items():
            for header in headers:
                if header.lower() in [name.lower() for name in possible_names]:
                    required_found[key] = header
                    break
        
        if "income_type" not in required_found or "amount" not in required_found:
            self.warnings.append(
                "CSV may not have standard columns. "
                "Expected: income_type, amount. Found: " + ", ".join(headers)
            )
        
        return True
    
    def extract_user_profile(self, data: Dict, year: int) -> UserProfile:
        """
        Extract UserProfile from CSV data.
        
        Args:
            data: Parsed CSV data
            year: Tax year
            
        Returns:
            UserProfile: Extracted user profile
        """
        rows = data["rows"]
        headers = data["headers"]
        
        # Map headers to our expected column names
        column_map = {}
        for key, possible_names in self.EXPECTED_COLUMNS.items():
            for header in headers:
                if header.lower() in [name.lower() for name in possible_names]:
                    column_map[key] = header
                    break
        
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
        
        # Process each row
        for row in rows:
            try:
                income_type = self._get_value(row, column_map.get("income_type", ""), "").lower()
                amount = self._parse_float(self._get_value(row, column_map.get("amount", ""), "0"))
                
                if amount <= 0:
                    continue
                
                # Map income types
                if "salary" in income_type or "employment" in income_type or "wage" in income_type:
                    months = self._parse_int(self._get_value(row, column_map.get("months", ""), "12"))
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
                    months = self._parse_int(self._get_value(row, column_map.get("months", ""), "12"))
                    monthly_rent = amount / months if months > 0 else amount / 12
                    rental.append(RentalIncome(
                        monthly_rent=monthly_rent,
                        months=months if months > 0 else 12,
                    ))
                    family_income += amount
                
                elif "capital" in income_type and "gain" in income_type:
                    # For capital gains, we need purchase and sale prices
                    # If only one amount is provided, assume it's the gain
                    purchase_price = self._parse_float(self._get_value(row, "purchase_price", "0"))
                    sale_price = self._parse_float(self._get_value(row, "sale_price", str(amount)))
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
                
                elif "property" in income_type:
                    property_value = amount
                    property_values.append(property_value)
                    property_type = self._get_value(row, "property_type", "residential").lower()
                    property_types.append(property_type)
            
            except Exception as e:
                self.warnings.append(f"Skipped row due to error: {str(e)}")
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
    
    def _get_value(self, row: Dict, key: str, default: str = "") -> str:
        """Get value from row, case-insensitive."""
        if not key:
            return default
        for k, v in row.items():
            if k.lower() == key.lower():
                return str(v) if v else default
        return default
    
    def _parse_float(self, value: str) -> float:
        """Parse float value, handling commas and spaces."""
        if not value:
            return 0.0
        # Remove commas and spaces
        cleaned = str(value).replace(",", "").replace(" ", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def _parse_int(self, value: str) -> int:
        """Parse integer value."""
        if not value:
            return 0
        try:
            return int(float(str(value).replace(",", "").strip()))
        except ValueError:
            return 0

