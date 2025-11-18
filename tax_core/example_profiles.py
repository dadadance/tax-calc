"""Example user profiles for quick testing and demonstration."""
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


EXAMPLE_PROFILES = {
    "typical_employee": {
        "name": "Typical Employee",
        "description": "Standard employee with salary and some rental income",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)
            ],
            rental=[
                RentalIncome(monthly_rent=1200.0, months=12, special_5_percent=True)
            ]
        )
    },
    
    "small_business_owner": {
        "name": "Small Business Owner",
        "description": "Entrepreneur with small business and part-time salary",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=3000.0, months=6, pension_employee_rate=0.02)
            ],
            small_business=[
                SmallBusinessIncome(turnover=600000.0, registered=True)
            ],
            property_tax=[
                PropertyTaxInput(family_income=80000.0, properties=2)
            ]
        )
    },
    
    "micro_business_eligible": {
        "name": "Micro Business (Eligible)",
        "description": "Micro business owner eligible for 0% tax",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            micro_business=[
                MicroBusinessIncome(
                    turnover=30000.0,
                    no_employees=True,
                    activity_allowed=True
                )
            ],
            dividends=[DividendsIncome(amount=5000.0)]
        )
    },
    
    "property_investor": {
        "name": "Property Investor",
        "description": "Multiple properties with rental income and capital gains",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            rental=[
                RentalIncome(monthly_rent=1000.0, months=12, special_5_percent=True),
                RentalIncome(monthly_rent=800.0, months=10, special_5_percent=True)
            ],
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=100000.0,
                    sale_price=120000.0,
                    is_primary_residence=False
                ),
                CapitalGainsIncome(
                    purchase_price=80000.0,
                    sale_price=95000.0,
                    is_primary_residence=False
                )
            ],
            property_tax=[
                PropertyTaxInput(family_income=90000.0, properties=3)
            ]
        )
    },
    
    "high_income_professional": {
        "name": "High Income Professional",
        "description": "High salary with multiple income sources",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=10000.0, months=12, pension_employee_rate=0.02)
            ],
            dividends=[DividendsIncome(amount=25000.0)],
            interest=[InterestIncome(amount=5000.0)],
            rental=[
                RentalIncome(monthly_rent=2000.0, months=12, special_5_percent=True)
            ],
            property_tax=[
                PropertyTaxInput(family_income=150000.0, properties=2)
            ]
        )
    },
    
    "retiree_with_investments": {
        "name": "Retiree with Investments",
        "description": "No salary, living off investments and property",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            dividends=[DividendsIncome(amount=20000.0)],
            interest=[InterestIncome(amount=8000.0)],
            rental=[
                RentalIncome(monthly_rent=1500.0, months=12, special_5_percent=True)
            ],
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=150000.0,
                    sale_price=180000.0,
                    is_primary_residence=True  # Exempt
                )
            ],
            property_tax=[
                PropertyTaxInput(family_income=50000.0, properties=1)  # Below threshold
            ]
        )
    },
    
    "complex_multi_income": {
        "name": "Complex Multi-Income",
        "description": "Multiple income types: salary, business, rental, investments",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=4000.0, months=12, pension_employee_rate=0.02)
            ],
            micro_business=[
                MicroBusinessIncome(turnover=25000.0, no_employees=True, activity_allowed=True)
            ],
            small_business=[
                SmallBusinessIncome(turnover=300000.0, registered=True)
            ],
            rental=[
                RentalIncome(monthly_rent=1000.0, months=12, special_5_percent=True)
            ],
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=20000.0,
                    sale_price=25000.0,
                    is_primary_residence=False
                ),
                CapitalGainsIncome(
                    purchase_price=15000.0,
                    sale_price=18000.0,
                    is_primary_residence=False
                )
            ],
            dividends=[DividendsIncome(amount=10000.0)],
            interest=[InterestIncome(amount=3000.0)],
            property_tax=[
                PropertyTaxInput(family_income=85000.0, properties=2)
            ]
        )
    },
    
    "non_resident": {
        "name": "Non-Resident",
        "description": "Non-resident with Georgian-source income",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.NON_RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=6000.0, months=12, pension_employee_rate=0.02)
            ],
            dividends=[DividendsIncome(amount=15000.0)],
            rental=[
                RentalIncome(monthly_rent=1500.0, months=8, special_5_percent=True)
            ]
        )
    },
    
    "low_income": {
        "name": "Low Income",
        "description": "Lower income with minimal tax burden",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=2000.0, months=12, pension_employee_rate=0.02)
            ],
            property_tax=[
                PropertyTaxInput(family_income=24000.0, properties=1)  # Below threshold
            ]
        )
    },
    
    "property_seller": {
        "name": "Property Seller",
        "description": "Selling multiple properties including primary residence",
        "profile": UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=4000.0, months=12, pension_employee_rate=0.02)
            ],
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=100000.0,
                    sale_price=120000.0,
                    is_primary_residence=False
                ),
                CapitalGainsIncome(
                    purchase_price=200000.0,
                    sale_price=250000.0,
                    is_primary_residence=True  # Exempt
                ),
                CapitalGainsIncome(
                    purchase_price=80000.0,
                    sale_price=95000.0,
                    is_primary_residence=False
                )
            ]
        )
    }
}


def get_example_profile(key: str) -> dict:
    """Get an example profile by key."""
    return EXAMPLE_PROFILES.get(key)


def get_all_profile_keys() -> list:
    """Get all available profile keys."""
    return list(EXAMPLE_PROFILES.keys())


def get_all_profiles() -> dict:
    """Get all example profiles."""
    return EXAMPLE_PROFILES

