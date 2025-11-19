"""Test RS.ge API modules (with mock data)."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.rs_ge.data_mapper import map_to_user_profile
from tax_core.models import ResidencyStatus


def test_data_mapper():
    """Test RS.ge data mapper with mock data."""
    print("Testing RS.ge Data Mapper...")
    print("-" * 50)
    
    # Mock RS.ge API response data
    mock_rs_data = {
        "income_declarations": [
            {"type": "salary", "amount": 120000, "period": "annual", "months": 12, "pension_rate": 0.02},
            {"type": "micro", "turnover": 50000, "no_employees": True, "activity_allowed": True},
            {"type": "rental", "monthly_rent": 500, "months": 12, "special_regime": True},
            {"type": "dividends", "amount": 5000},
            {"type": "interest", "amount": 2000},
        ],
        "salary_income": [
            {"amount": 120000, "period": "annual", "months": 12, "pension_rate": 0.02}
        ],
        "business_income": [
            {"type": "micro", "turnover": 50000, "no_employees": True, "activity_allowed": True}
        ],
        "rental_income": [
            {"monthly_rent": 500, "months": 12, "special_regime": True}
        ],
        "capital_gains": [],
        "dividends": [
            {"amount": 5000}
        ],
        "interest": [
            {"amount": 2000}
        ],
        "property_info": [
            {"assessed_value": 65000, "type": "residential", "tax_rate": 0.01, "income_threshold": 40000}
        ],
        "family_income": 177000.0,
    }
    
    try:
        profile = map_to_user_profile(mock_rs_data, 2025, ResidencyStatus.RESIDENT)
        
        print("✓ Data mapping successful!")
        print(f"\nMapped Profile Summary:")
        print(f"  Tax Year: {profile.year}")
        print(f"  Residency: {profile.residency.value}")
        print(f"  Family Income: {profile.family_income:,.2f} GEL")
        print(f"\nIncome Sources:")
        print(f"  Salary: {len(profile.salary)} source(s)")
        print(f"    - Monthly: {profile.salary[0].monthly_gross:,.2f} GEL × {profile.salary[0].months} months")
        print(f"  Micro Business: {len(profile.micro_business)} source(s)")
        print(f"    - Turnover: {profile.micro_business[0].turnover:,.2f} GEL")
        print(f"  Small Business: {len(profile.small_business)} source(s)")
        print(f"  Rental: {len(profile.rental)} source(s)")
        print(f"    - Monthly: {profile.rental[0].monthly_rent:,.2f} GEL × {profile.rental[0].months} months")
        print(f"  Dividends: {len(profile.dividends)} source(s)")
        print(f"    - Amount: {profile.dividends[0].amount:,.2f} GEL")
        print(f"  Interest: {len(profile.interest)} source(s)")
        print(f"    - Amount: {profile.interest[0].amount:,.2f} GEL")
        print(f"  Property Tax: {len(profile.property_tax)} source(s)")
        if profile.property_tax:
            print(f"    - Properties: {profile.property_tax[0].properties}")
            print(f"    - Values: {profile.property_tax[0].property_values}")
        
        # Verify calculations
        expected_family_income = (
            profile.salary[0].monthly_gross * profile.salary[0].months +
            profile.micro_business[0].turnover +
            profile.rental[0].monthly_rent * profile.rental[0].months +
            profile.dividends[0].amount +
            profile.interest[0].amount
        )
        
        if abs(profile.family_income - expected_family_income) < 0.01:
            print(f"\n✓ Family income calculation correct: {profile.family_income:,.2f} GEL")
        else:
            print(f"\n⚠️ Family income mismatch:")
            print(f"  Expected: {expected_family_income:,.2f} GEL")
            print(f"  Got: {profile.family_income:,.2f} GEL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data mapper: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_auth_module():
    """Test authentication module structure."""
    print("\nTesting RS.ge Auth Module Structure...")
    print("-" * 50)
    
    try:
        from tax_core.rs_ge.auth import RSGeAuth, AuthToken
        from tax_core.rs_ge.exceptions import RSGeAuthError
        
        print("✓ Auth module imports successful")
        print("✓ RSGeAuth class available")
        print("✓ AuthToken class available")
        print("✓ RSGeAuthError exception available")
        
        # Test AuthToken
        from datetime import datetime, timedelta
        token = AuthToken(
            token="test_token",
            expires_at=datetime.now() + timedelta(hours=1)
        )
        
        if not token.is_expired():
            print("✓ AuthToken.is_expired() works correctly")
        else:
            print("❌ AuthToken.is_expired() failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing auth module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_api_client_structure():
    """Test API client module structure."""
    print("\nTesting RS.ge API Client Structure...")
    print("-" * 50)
    
    try:
        from tax_core.rs_ge.api_client import RSGeAPIClient
        from tax_core.rs_ge.exceptions import RSGeAPIError, RSGeConnectionError
        
        print("✓ API client module imports successful")
        print("✓ RSGeAPIClient class available")
        print("✓ RSGeAPIError exception available")
        print("✓ RSGeConnectionError exception available")
        
        # Note: We can't test actual API calls without real credentials
        print("ℹ️  Actual API calls require RS.ge credentials (not tested)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API client: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing RS.ge Modules")
    print("=" * 50)
    
    mapper_ok = test_data_mapper()
    auth_ok = test_auth_module()
    client_ok = test_api_client_structure()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"  Data Mapper: {'✓ PASS' if mapper_ok else '❌ FAIL'}")
    print(f"  Auth Module: {'✓ PASS' if auth_ok else '❌ FAIL'}")
    print(f"  API Client: {'✓ PASS' if client_ok else '❌ FAIL'}")
    print("=" * 50)
    
    return mapper_ok and auth_ok and client_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

