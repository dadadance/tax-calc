#!/usr/bin/env python3
"""Automated testing script for the tax calculator app."""
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
from tax_core.calculators import calculate_all
from tax_core.error_logger import log_app_error


class AppTester:
    """Automated tester for the tax calculator."""
    
    def __init__(self):
        """Initialize the tester."""
        self.test_results = []
        self.errors = []
    
    def run_test(self, test_name: str, test_func):
        """Run a test and record results."""
        print(f"Running test: {test_name}...", end=" ")
        try:
            result = test_func()
            self.test_results.append({
                "name": test_name,
                "status": "PASSED",
                "result": result
            })
            print("✓ PASSED")
            return result
        except Exception as e:
            self.test_results.append({
                "name": test_name,
                "status": "FAILED",
                "error": str(e)
            })
            self.errors.append((test_name, e))
            log_app_error(e, user_action=f"Test: {test_name}")
            print(f"✗ FAILED: {e}")
            return None
    
    def test_salary_calculation(self):
        """Test salary calculation."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=3000.0, months=12, pension_employee_rate=0.02)
            ]
        )
        result = calculate_all(profile)
        assert result.total_tax > 0, "Tax should be greater than 0"
        assert result.total_income == 36000.0, f"Expected 36000, got {result.total_income}"
        assert len(result.by_regime) > 0, "Should have at least one regime result"
        return result
    
    def test_micro_business_zero_tax(self):
        """Test micro business with 0% tax."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            micro_business=[
                MicroBusinessIncome(
                    turnover=25000.0,
                    no_employees=True,
                    activity_allowed=True
                )
            ]
        )
        result = calculate_all(profile)
        # Micro business should have 0% tax if eligible
        micro_regime = next((r for r in result.by_regime if r.regime_id == "micro_business"), None)
        assert micro_regime is not None, "Should have micro_business regime"
        assert micro_regime.tax == 0.0, f"Expected 0 tax, got {micro_regime.tax}"
        return result
    
    def test_small_business_threshold(self):
        """Test small business with turnover above threshold."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            small_business=[
                SmallBusinessIncome(turnover=600000.0, registered=True)
            ]
        )
        result = calculate_all(profile)
        small_regime = next((r for r in result.by_regime if r.regime_id == "small_business"), None)
        assert small_regime is not None, "Should have small_business regime"
        # 1% on 500k + 3% on 100k = 5000 + 3000 = 8000
        expected_tax = 500000 * 0.01 + 100000 * 0.03
        assert abs(small_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax}, got {small_regime.tax}"
        return result
    
    def test_rental_5_percent(self):
        """Test rental income with 5% regime."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            rental=[
                RentalIncome(monthly_rent=800.0, months=12, special_5_percent=True)
            ]
        )
        result = calculate_all(profile)
        rental_regime = next((r for r in result.by_regime if r.regime_id == "rental"), None)
        assert rental_regime is not None, "Should have rental regime"
        expected_tax = 800 * 12 * 0.05  # 480
        assert abs(rental_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax}, got {rental_regime.tax}"
        return result
    
    def test_capital_gains(self):
        """Test capital gains calculation."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=100000.0,
                    sale_price=120000.0,
                    is_primary_residence=False
                )
            ]
        )
        result = calculate_all(profile)
        cg_regime = next((r for r in result.by_regime if r.regime_id == "capital_gains"), None)
        assert cg_regime is not None, "Should have capital_gains regime"
        expected_tax = 20000 * 0.05  # 1000
        assert abs(cg_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax}, got {cg_regime.tax}"
        return result
    
    def test_dividends_and_interest(self):
        """Test dividends and interest."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            dividends=[DividendsIncome(amount=5000.0)],
            interest=[InterestIncome(amount=1000.0)]
        )
        result = calculate_all(profile)
        dividends_regime = next((r for r in result.by_regime if r.regime_id == "dividends"), None)
        interest_regime = next((r for r in result.by_regime if r.regime_id == "interest"), None)
        assert dividends_regime is not None, "Should have dividends regime"
        assert interest_regime is not None, "Should have interest regime"
        assert abs(dividends_regime.tax - 250.0) < 0.01, "Dividends tax should be 250"
        assert abs(interest_regime.tax - 50.0) < 0.01, "Interest tax should be 50"
        return result
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple income types."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)],
            micro_business=[MicroBusinessIncome(turnover=30000.0, no_employees=True, activity_allowed=True)],
            rental=[RentalIncome(monthly_rent=1000.0, months=12, special_5_percent=True)],
            dividends=[DividendsIncome(amount=10000.0)]
        )
        result = calculate_all(profile)
        assert result.total_tax > 0, "Should have total tax"
        assert result.total_income > 0, "Should have total income"
        assert result.effective_rate > 0, "Should have effective rate"
        return result
    
    def test_empty_profile(self):
        """Test empty profile (no income)."""
        profile = UserProfile(year=2025, residency=ResidencyStatus.RESIDENT)
        result = calculate_all(profile)
        assert result.total_tax == 0.0, "Tax should be 0 with no income"
        assert result.total_income == 0.0, "Income should be 0"
        assert len(result.by_regime) == 0, "Should have no regime results"
        return result
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Zero values
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[SalaryIncome(monthly_gross=0.0, months=12)]
        )
        result = calculate_all(profile)
        assert result.total_tax == 0.0, "Tax should be 0 with zero income"
        
        # Negative capital gain (loss)
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            capital_gains=[
                CapitalGainsIncome(purchase_price=100000.0, sale_price=80000.0)
            ]
        )
        result = calculate_all(profile)
        cg_regime = next((r for r in result.by_regime if r.regime_id == "capital_gains"), None)
        if cg_regime:
            assert cg_regime.tax == 0.0, "Tax should be 0 on capital loss"
        
        return result
    
    def test_multiple_salary_sources(self):
        """Test multiple salary sources."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=2000.0, months=6, pension_employee_rate=0.02),
                SalaryIncome(monthly_gross=4000.0, months=6, pension_employee_rate=0.02)
            ]
        )
        result = calculate_all(profile)
        assert result.total_income == 2000 * 6 + 4000 * 6, "Total income should be sum of both"
        assert result.total_tax > 0, "Should have tax"
        salary_regime = next((r for r in result.by_regime if r.regime_id == "salary"), None)
        assert salary_regime is not None, "Should have salary regime"
        assert len(salary_regime.steps) >= 4, "Should have steps for both salaries"
        return result
    
    def test_micro_business_fallback(self):
        """Test micro business fallback to 20% when conditions not met."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            micro_business=[
                MicroBusinessIncome(
                    turnover=30000.0,
                    no_employees=False,  # Has employees - not eligible
                    activity_allowed=True
                )
            ]
        )
        result = calculate_all(profile)
        micro_regime = next((r for r in result.by_regime if r.regime_id == "micro_business"), None)
        assert micro_regime is not None, "Should have micro_business regime"
        expected_tax = 30000 * 0.20  # 20% fallback
        assert abs(micro_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax} tax (20% fallback), got {micro_regime.tax}"
        assert len(micro_regime.warnings) > 0, "Should have warnings"
        return result
    
    def test_small_business_below_threshold(self):
        """Test small business below 500k threshold."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            small_business=[
                SmallBusinessIncome(turnover=300000.0, registered=True)
            ]
        )
        result = calculate_all(profile)
        small_regime = next((r for r in result.by_regime if r.regime_id == "small_business"), None)
        assert small_regime is not None, "Should have small_business regime"
        expected_tax = 300000 * 0.01  # 1% on full amount
        assert abs(small_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax} tax (1%), got {small_regime.tax}"
        return result
    
    def test_rental_standard_rate(self):
        """Test rental income with standard 20% rate."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            rental=[
                RentalIncome(monthly_rent=1000.0, months=12, special_5_percent=False)
            ]
        )
        result = calculate_all(profile)
        rental_regime = next((r for r in result.by_regime if r.regime_id == "rental"), None)
        assert rental_regime is not None, "Should have rental regime"
        expected_tax = 1000 * 12 * 0.20  # 20% standard
        assert abs(rental_regime.tax - expected_tax) < 0.01, \
            f"Expected {expected_tax} tax (20%), got {rental_regime.tax}"
        return result
    
    def test_primary_residence_exemption(self):
        """Test capital gains with primary residence exemption."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=80000.0,
                    sale_price=150000.0,
                    is_primary_residence=True  # Exempt
                )
            ]
        )
        result = calculate_all(profile)
        cg_regime = next((r for r in result.by_regime if r.regime_id == "capital_gains"), None)
        assert cg_regime is not None, "Should have capital_gains regime"
        assert cg_regime.tax == 0.0, "Tax should be 0 for primary residence"
        return result
    
    def test_property_tax_below_threshold(self):
        """Test property tax below income threshold."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            property_tax=[
                PropertyTaxInput(family_income=50000.0, properties=2)  # Below 65k threshold
            ]
        )
        result = calculate_all(profile)
        prop_regime = next((r for r in result.by_regime if r.regime_id == "property_tax"), None)
        assert prop_regime is not None, "Should have property_tax regime"
        # Should have steps showing exemption
        assert len(prop_regime.steps) > 0, "Should have calculation steps"
        return result
    
    def test_non_resident(self):
        """Test non-resident calculation."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.NON_RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)
            ]
        )
        result = calculate_all(profile)
        assert result.residency == ResidencyStatus.NON_RESIDENT, "Should be non-resident"
        assert result.total_tax > 0, "Should have tax"
        return result
    
    def test_effective_rate_calculation(self):
        """Test effective tax rate calculation."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=10000.0, months=12, pension_employee_rate=0.02)
            ]
        )
        result = calculate_all(profile)
        assert result.total_income == 120000.0, "Income should be 120k"
        expected_tax = 120000 * 0.20  # 20% PIT
        assert abs(result.total_tax - expected_tax) < 0.01, "Tax should be 20%"
        expected_rate = expected_tax / result.total_income
        assert abs(result.effective_rate - expected_rate) < 0.0001, \
            f"Effective rate should be ~{expected_rate}, got {result.effective_rate}"
        return result
    
    def test_calculation_steps_present(self):
        """Test that calculation steps are present and correct."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)
            ]
        )
        result = calculate_all(profile)
        salary_regime = next((r for r in result.by_regime if r.regime_id == "salary"), None)
        assert salary_regime is not None, "Should have salary regime"
        assert len(salary_regime.steps) >= 3, "Should have at least 3 steps (gross, pension, pit)"
        
        # Check step IDs
        step_ids = [s.id for s in salary_regime.steps]
        assert "salary_0_gross" in step_ids, "Should have gross calculation step"
        assert "salary_0_pit" in step_ids, "Should have PIT calculation step"
        
        # Check step results
        gross_step = next((s for s in salary_regime.steps if "gross" in s.id), None)
        assert gross_step is not None, "Should have gross step"
        assert gross_step.result == 60000.0, "Gross should be 60k"
        
        return result
    
    def test_warnings_generation(self):
        """Test that warnings are generated appropriately."""
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            small_business=[
                SmallBusinessIncome(turnover=600000.0, registered=True)  # Above threshold
            ]
        )
        result = calculate_all(profile)
        small_regime = next((r for r in result.by_regime if r.regime_id == "small_business"), None)
        assert small_regime is not None, "Should have small_business regime"
        # Should have warning about exceeding threshold
        assert len(small_regime.warnings) > 0, "Should have warnings"
        return result
    
    def run_all_tests(self):
        """Run all tests."""
        print("=" * 80)
        print("TAX CALCULATOR AUTOMATED TESTS")
        print("=" * 80)
        print()
        
        tests = [
            ("Salary Calculation", self.test_salary_calculation),
            ("Multiple Salary Sources", self.test_multiple_salary_sources),
            ("Micro Business Zero Tax", self.test_micro_business_zero_tax),
            ("Micro Business Fallback", self.test_micro_business_fallback),
            ("Small Business Below Threshold", self.test_small_business_below_threshold),
            ("Small Business Threshold", self.test_small_business_threshold),
            ("Rental 5% Regime", self.test_rental_5_percent),
            ("Rental Standard Rate", self.test_rental_standard_rate),
            ("Capital Gains", self.test_capital_gains),
            ("Primary Residence Exemption", self.test_primary_residence_exemption),
            ("Dividends and Interest", self.test_dividends_and_interest),
            ("Property Tax Below Threshold", self.test_property_tax_below_threshold),
            ("Non-Resident", self.test_non_resident),
            ("Effective Rate Calculation", self.test_effective_rate_calculation),
            ("Calculation Steps Present", self.test_calculation_steps_present),
            ("Warnings Generation", self.test_warnings_generation),
            ("Complex Scenario", self.test_complex_scenario),
            ("Empty Profile", self.test_empty_profile),
            ("Edge Cases", self.test_edge_cases),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            time.sleep(0.1)  # Small delay between tests
        
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in self.test_results if r["status"] == "PASSED")
        failed = sum(1 for r in self.test_results if r["status"] == "FAILED")
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  - {result['name']}: {result.get('error', 'Unknown error')}")
        
        print("=" * 80)
        
        return failed == 0


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run automated tests for tax calculator")
    parser.add_argument(
        "--test",
        type=str,
        help="Run specific test by name"
    )
    
    args = parser.parse_args()
    
    tester = AppTester()
    
    if args.test:
        # Run specific test
        test_method = getattr(tester, f"test_{args.test.lower().replace(' ', '_')}", None)
        if test_method:
            tester.run_test(args.test, test_method)
        else:
            print(f"Test '{args.test}' not found.")
            print("Available tests:")
            for method in dir(tester):
                if method.startswith("test_"):
                    print(f"  - {method[5:]}")
    else:
        # Run all tests
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

