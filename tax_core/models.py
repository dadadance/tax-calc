"""Data models for tax calculations."""
from dataclasses import dataclass, field
from typing import List, Optional, Literal
from enum import Enum


class ResidencyStatus(str, Enum):
    """Residency status."""
    RESIDENT = "RESIDENT"
    NON_RESIDENT = "NON_RESIDENT"


@dataclass
class SalaryIncome:
    """Salary income input."""
    monthly_gross: float = 0.0
    months: int = 12
    pension_employee_rate: float = 0.02


@dataclass
class MicroBusinessIncome:
    """Micro business income input."""
    turnover: float = 0.0
    no_employees: bool = True
    activity_allowed: bool = True


@dataclass
class SmallBusinessIncome:
    """Small business income input."""
    turnover: float = 0.0
    registered: bool = True


@dataclass
class RentalIncome:
    """Rental income input."""
    monthly_rent: float = 0.0
    months: int = 12
    special_5_percent: bool = True


@dataclass
class CapitalGainsIncome:
    """Capital gains income input."""
    purchase_price: float = 0.0
    sale_price: float = 0.0
    purchase_date: Optional[str] = None
    sale_date: Optional[str] = None
    is_primary_residence: bool = False


@dataclass
class DividendsIncome:
    """Dividends income input."""
    amount: float = 0.0


@dataclass
class InterestIncome:
    """Interest income input."""
    amount: float = 0.0


@dataclass
class PropertyTaxInput:
    """Property tax input."""
    family_income: float = 0.0
    properties: int = 0
    property_values: List[float] = field(default_factory=list)  # List of property values (market value or purchase price)
    tax_rate: float = 0.01  # Property tax rate (default 1%, can be adjusted by municipality)
    income_threshold: float = 40000.0  # Income threshold for property tax (RS.ge: 40,000 GEL individual income)
    # Note: Some sources indicate 65,000 GEL for family income - verify with RS.ge


@dataclass
class UserProfile:
    """User profile and income inputs."""
    year: int = 2025
    residency: ResidencyStatus = ResidencyStatus.RESIDENT
    family_income: float = 0.0
    
    # Income sources
    salary: List[SalaryIncome] = None
    micro_business: List[MicroBusinessIncome] = None
    small_business: List[SmallBusinessIncome] = None
    rental: List[RentalIncome] = None
    capital_gains: List[CapitalGainsIncome] = None
    dividends: List[DividendsIncome] = None
    interest: List[InterestIncome] = None
    property_tax: List[PropertyTaxInput] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.salary is None:
            self.salary = []
        if self.micro_business is None:
            self.micro_business = []
        if self.small_business is None:
            self.small_business = []
        if self.rental is None:
            self.rental = []
        if self.capital_gains is None:
            self.capital_gains = []
        if self.dividends is None:
            self.dividends = []
        if self.interest is None:
            self.interest = []
        if self.property_tax is None:
            self.property_tax = []


@dataclass
class CalculationStep:
    """A single step in the calculation."""
    id: str
    description: str
    formula: str
    values: str
    result: float
    legal_ref: Optional[str] = None


@dataclass
class RegimeResult:
    """Result for a specific tax regime."""
    regime_id: str
    tax: float
    steps: List[CalculationStep]
    warnings: List[str] = None
    
    def __post_init__(self):
        """Initialize empty warnings list if None."""
        if self.warnings is None:
            self.warnings = []


@dataclass
class CalculationResult:
    """Complete calculation result."""
    year: int
    rules_version: str
    residency: ResidencyStatus
    total_tax: float
    effective_rate: float
    by_regime: List[RegimeResult]
    total_income: float = 0.0

