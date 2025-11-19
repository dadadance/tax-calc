"""Map RS.ge API data to our UserProfile model."""
from typing import Dict, List, Tuple
from datetime import datetime
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
from tax_core.rs_ge.exceptions import RSGeDataError


def map_to_user_profile(rs_data: Dict, year: int, residency: ResidencyStatus = ResidencyStatus.RESIDENT) -> UserProfile:
    """
    Map RS.ge API data to UserProfile.
    
    Args:
        rs_data: Dictionary containing RS.ge API response data
        year: Tax year
        residency: Residency status
        
    Returns:
        UserProfile: Mapped user profile
        
    Raises:
        RSGeDataError: If data mapping fails
    """
    try:
        # Extract income declarations
        income_declarations = rs_data.get("income_declarations", [])
        
        # Map salary income
        salary = map_salary_income(rs_data.get("salary_income", []))
        
        # Map business income
        micro_business, small_business = map_business_income(rs_data.get("business_income", []))
        
        # Map rental income
        rental = map_rental_income(rs_data.get("rental_income", []))
        
        # Map capital gains
        capital_gains = map_capital_gains(rs_data.get("capital_gains", []))
        
        # Map dividends
        dividends = map_dividends(rs_data.get("dividends", []))
        
        # Map interest
        interest = map_interest(rs_data.get("interest", []))
        
        # Map property tax info
        property_tax = map_property_info(rs_data.get("property_info", []), rs_data.get("family_income", 0.0))
        
        # Calculate total family income
        family_income = (
            sum(s.monthly_gross * s.months for s in salary) +
            sum(m.turnover for m in micro_business) +
            sum(s.turnover for s in small_business) +
            sum(r.monthly_rent * r.months for r in rental) +
            sum(max(0, cg.sale_price - cg.purchase_price) for cg in capital_gains) +
            sum(d.amount for d in dividends) +
            sum(i.amount for i in interest)
        )
        
        return UserProfile(
            year=year,
            residency=residency,
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
        
    except Exception as e:
        raise RSGeDataError(f"Failed to map RS.ge data to UserProfile: {str(e)}")


def map_salary_income(rs_data: List[Dict]) -> List[SalaryIncome]:
    """
    Map RS.ge salary income data to SalaryIncome models.
    
    Args:
        rs_data: List of salary income records from RS.ge
        
    Returns:
        List[SalaryIncome]: Mapped salary income records
    """
    salary_list = []
    
    for record in rs_data:
        try:
            # RS.ge may provide annual or monthly amounts
            amount = float(record.get("amount", 0))
            period = record.get("period", "annual").lower()
            
            if period == "monthly":
                monthly_gross = amount
                months = int(record.get("months", 12))
            else:  # annual
                monthly_gross = amount / 12
                months = 12
            
            salary_list.append(SalaryIncome(
                monthly_gross=monthly_gross,
                months=months,
                pension_employee_rate=float(record.get("pension_rate", 0.02)),
            ))
        except (ValueError, KeyError) as e:
            # Skip invalid records, log warning
            continue
    
    return salary_list


def map_business_income(rs_data: List[Dict]) -> Tuple[List[MicroBusinessIncome], List[SmallBusinessIncome]]:
    """
    Map RS.ge business income data to business income models.
    
    Args:
        rs_data: List of business income records from RS.ge
        
    Returns:
        Tuple of (MicroBusinessIncome list, SmallBusinessIncome list)
    """
    micro_list = []
    small_list = []
    
    for record in rs_data:
        try:
            turnover = float(record.get("turnover", 0))
            business_type = record.get("type", "").lower()
            
            if business_type == "micro":
                micro_list.append(MicroBusinessIncome(
                    turnover=turnover,
                    no_employees=bool(record.get("no_employees", True)),
                    activity_allowed=bool(record.get("activity_allowed", True)),
                ))
            elif business_type == "small":
                small_list.append(SmallBusinessIncome(
                    turnover=turnover,
                    registered=bool(record.get("registered", True)),
                ))
        except (ValueError, KeyError):
            continue
    
    return micro_list, small_list


def map_rental_income(rs_data: List[Dict]) -> List[RentalIncome]:
    """
    Map RS.ge rental income data to RentalIncome models.
    
    Args:
        rs_data: List of rental income records from RS.ge
        
    Returns:
        List[RentalIncome]: Mapped rental income records
    """
    rental_list = []
    
    for record in rs_data:
        try:
            monthly_rent = float(record.get("monthly_rent", 0))
            months = int(record.get("months", 12))
            
            rental_list.append(RentalIncome(
                monthly_rent=monthly_rent,
                months=months,
                special_5_percent=bool(record.get("special_regime", True)),
            ))
        except (ValueError, KeyError):
            continue
    
    return rental_list


def map_capital_gains(rs_data: List[Dict]) -> List[CapitalGainsIncome]:
    """
    Map RS.ge capital gains data to CapitalGainsIncome models.
    
    Args:
        rs_data: List of capital gains records from RS.ge
        
    Returns:
        List[CapitalGainsIncome]: Mapped capital gains records
    """
    cg_list = []
    
    for record in rs_data:
        try:
            purchase_price = float(record.get("purchase_price", 0))
            sale_price = float(record.get("sale_price", 0))
            
            cg_list.append(CapitalGainsIncome(
                purchase_price=purchase_price,
                sale_price=sale_price,
                purchase_date=record.get("purchase_date"),
                sale_date=record.get("sale_date"),
                is_primary_residence=bool(record.get("is_primary_residence", False)),
            ))
        except (ValueError, KeyError):
            continue
    
    return cg_list


def map_dividends(rs_data: List[Dict]) -> List[DividendsIncome]:
    """
    Map RS.ge dividends data to DividendsIncome models.
    
    Args:
        rs_data: List of dividends records from RS.ge
        
    Returns:
        List[DividendsIncome]: Mapped dividends records
    """
    return [
        DividendsIncome(amount=float(record.get("amount", 0)))
        for record in rs_data
        if record.get("amount")
    ]


def map_interest(rs_data: List[Dict]) -> List[InterestIncome]:
    """
    Map RS.ge interest data to InterestIncome models.
    
    Args:
        rs_data: List of interest records from RS.ge
        
    Returns:
        List[InterestIncome]: Mapped interest records
    """
    return [
        InterestIncome(amount=float(record.get("amount", 0)))
        for record in rs_data
        if record.get("amount")
    ]


def map_property_info(rs_data: List[Dict], family_income: float) -> List[PropertyTaxInput]:
    """
    Map RS.ge property information to PropertyTaxInput models.
    
    Args:
        rs_data: List of property records from RS.ge
        family_income: Total family income
        
    Returns:
        List[PropertyTaxInput]: Mapped property tax inputs
    """
    if not rs_data:
        return []
    
    # Extract property values and types
    property_values = []
    property_types = []
    
    for record in rs_data:
        try:
            value = float(record.get("assessed_value", record.get("market_value", 0)))
            if value > 0:
                property_values.append(value)
                property_types.append(record.get("type", "residential").lower())
        except (ValueError, KeyError):
            continue
    
    if not property_values:
        return []
    
    # Get tax rate (may vary by municipality)
    tax_rate = float(rs_data[0].get("tax_rate", 0.01))
    
    # Get income threshold
    income_threshold = float(rs_data[0].get("income_threshold", 40000.0))
    
    return [PropertyTaxInput(
        family_income=family_income,
        properties=len(property_values),
        property_values=property_values,
        property_types=property_types,
        tax_rate=tax_rate,
        income_threshold=income_threshold,
    )]

