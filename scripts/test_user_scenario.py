#!/usr/bin/env python3
"""Test script for typical user scenarios - simulates real user interactions."""
import sys
from pathlib import Path

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


class UserScenarioTester:
    """Test typical user scenarios."""
    
    def __init__(self):
        """Initialize the tester."""
        self.test_results = []
        self.errors = []
    
    def run_scenario(self, scenario_name: str, scenario_func):
        """Run a user scenario and record results."""
        print(f"\n{'='*80}")
        print(f"Scenario: {scenario_name}")
        print(f"{'='*80}")
        try:
            result = scenario_func()
            self.test_results.append({
                "name": scenario_name,
                "status": "PASSED",
                "result": result
            })
            print(f"✓ Scenario PASSED")
            return result
        except Exception as e:
            self.test_results.append({
                "name": scenario_name,
                "status": "FAILED",
                "error": str(e)
            })
            self.errors.append((scenario_name, e))
            log_app_error(e, user_action=f"User Scenario: {scenario_name}")
            print(f"✗ Scenario FAILED: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def scenario_typical_resident(self):
        """Scenario: Typical resident with salary and rental income."""
        print("\n📋 User Profile:")
        print("   - Resident")
        print("   - Salary: 5,000 GEL/month × 12 months")
        print("   - Rental: 1,200 GEL/month × 12 months (5% regime)")
        print("   - Dividends: 10,000 GEL")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)
            ],
            rental=[
                RentalIncome(monthly_rent=1200.0, months=12, special_5_percent=True)
            ],
            dividends=[DividendsIncome(amount=10000.0)]
        )
        
        result = calculate_all(profile)
        
        # Verify expectations
        expected_salary_income = 5000 * 12  # 60,000
        expected_rental_income = 1200 * 12  # 14,400
        expected_total_income = expected_salary_income + expected_rental_income + 10000  # 84,400
        
        assert abs(result.total_income - expected_total_income) < 0.01, \
            f"Expected total income {expected_total_income}, got {result.total_income}"
        
        expected_salary_tax = expected_salary_income * 0.20  # 12,000
        expected_rental_tax = expected_rental_income * 0.05  # 720
        expected_dividends_tax = 10000 * 0.05  # 500
        expected_total_tax = expected_salary_tax + expected_rental_tax + expected_dividends_tax  # 13,220
        
        assert abs(result.total_tax - expected_total_tax) < 0.01, \
            f"Expected total tax {expected_total_tax}, got {result.total_tax}"
        
        # Verify regimes present
        regime_ids = [r.regime_id for r in result.by_regime]
        assert "salary" in regime_ids, "Should have salary regime"
        assert "rental" in regime_ids, "Should have rental regime"
        assert "dividends" in regime_ids, "Should have dividends regime"
        
        # Verify calculation steps
        salary_regime = next(r for r in result.by_regime if r.regime_id == "salary")
        assert len(salary_regime.steps) >= 3, "Salary should have calculation steps"
        
        print(f"\n✓ Results:")
        print(f"   Total Income: {result.total_income:,.2f} GEL")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        print(f"   Effective Rate: {result.effective_rate * 100:.2f}%")
        print(f"   Regimes: {len(result.by_regime)}")
        
        return result
    
    def scenario_small_business_owner(self):
        """Scenario: Small business owner with turnover above threshold."""
        print("\n📋 User Profile:")
        print("   - Resident")
        print("   - Small Business: 600,000 GEL turnover")
        print("   - Salary: 3,000 GEL/month × 6 months (part-time)")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            small_business=[
                SmallBusinessIncome(turnover=600000.0, registered=True)
            ],
            salary=[
                SalaryIncome(monthly_gross=3000.0, months=6, pension_employee_rate=0.02)
            ]
        )
        
        result = calculate_all(profile)
        
        # Verify small business tax (1% on 500k + 3% on 100k)
        small_regime = next((r for r in result.by_regime if r.regime_id == "small_business"), None)
        assert small_regime is not None, "Should have small business regime"
        
        expected_small_tax = 500000 * 0.01 + 100000 * 0.03  # 5,000 + 3,000 = 8,000
        assert abs(small_regime.tax - expected_small_tax) < 0.01, \
            f"Expected small business tax {expected_small_tax}, got {small_regime.tax}"
        
        # Should have warning about threshold
        assert len(small_regime.warnings) > 0, "Should have warning about exceeding threshold"
        
        print(f"\n✓ Results:")
        print(f"   Small Business Tax: {small_regime.tax:,.2f} GEL")
        print(f"   Warnings: {len(small_regime.warnings)}")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        
        return result
    
    def scenario_micro_business_eligible(self):
        """Scenario: Micro business owner eligible for 0% tax."""
        print("\n📋 User Profile:")
        print("   - Resident")
        print("   - Micro Business: 30,000 GEL turnover")
        print("   - No employees, allowed activity")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            micro_business=[
                MicroBusinessIncome(
                    turnover=30000.0,
                    no_employees=True,
                    activity_allowed=True
                )
            ]
        )
        
        result = calculate_all(profile)
        
        micro_regime = next((r for r in result.by_regime if r.regime_id == "micro_business"), None)
        assert micro_regime is not None, "Should have micro business regime"
        assert micro_regime.tax == 0.0, "Micro business should have 0% tax when eligible"
        
        print(f"\n✓ Results:")
        print(f"   Micro Business Tax: {micro_regime.tax:,.2f} GEL (0% - eligible)")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        
        return result
    
    def scenario_property_seller(self):
        """Scenario: Person selling property with capital gains."""
        print("\n📋 User Profile:")
        print("   - Resident")
        print("   - Capital Gain: Purchased 100k, Sold 150k")
        print("   - Not primary residence")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            capital_gains=[
                CapitalGainsIncome(
                    purchase_price=100000.0,
                    sale_price=150000.0,
                    is_primary_residence=False
                )
            ]
        )
        
        result = calculate_all(profile)
        
        cg_regime = next((r for r in result.by_regime if r.regime_id == "capital_gains"), None)
        assert cg_regime is not None, "Should have capital gains regime"
        
        expected_gain = 150000 - 100000  # 50,000
        expected_tax = expected_gain * 0.05  # 2,500
        
        assert abs(cg_regime.tax - expected_tax) < 0.01, \
            f"Expected capital gains tax {expected_tax}, got {cg_regime.tax}"
        
        print(f"\n✓ Results:")
        print(f"   Capital Gain: {expected_gain:,.2f} GEL")
        print(f"   Capital Gains Tax: {cg_regime.tax:,.2f} GEL (5%)")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        
        return result
    
    def scenario_complex_multi_income(self):
        """Scenario: Complex scenario with multiple income types."""
        print("\n📋 User Profile:")
        print("   - Resident")
        print("   - Salary: 4,000 GEL/month × 12 months")
        print("   - Micro Business: 25,000 GEL (eligible)")
        print("   - Rental: 800 GEL/month × 12 months (5%)")
        print("   - Dividends: 5,000 GEL")
        print("   - Interest: 2,000 GEL")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=4000.0, months=12, pension_employee_rate=0.02)
            ],
            micro_business=[
                MicroBusinessIncome(turnover=25000.0, no_employees=True, activity_allowed=True)
            ],
            rental=[
                RentalIncome(monthly_rent=800.0, months=12, special_5_percent=True)
            ],
            dividends=[DividendsIncome(amount=5000.0)],
            interest=[InterestIncome(amount=2000.0)]
        )
        
        result = calculate_all(profile)
        
        # Verify all regimes present
        regime_ids = [r.regime_id for r in result.by_regime]
        assert "salary" in regime_ids, "Should have salary"
        assert "micro_business" in regime_ids, "Should have micro business"
        assert "rental" in regime_ids, "Should have rental"
        assert "dividends" in regime_ids, "Should have dividends"
        assert "interest" in regime_ids, "Should have interest"
        
        # Verify micro business is 0%
        micro_regime = next(r for r in result.by_regime if r.regime_id == "micro_business")
        assert micro_regime.tax == 0.0, "Micro business should be 0%"
        
        # Calculate expected totals
        salary_income = 4000 * 12  # 48,000
        micro_income = 25000  # 25,000 (but 0% tax)
        rental_income = 800 * 12  # 9,600
        dividends_income = 5000  # 5,000
        interest_income = 2000  # 2,000
        total_income = salary_income + micro_income + rental_income + dividends_income + interest_income  # 89,600
        
        assert abs(result.total_income - total_income) < 0.01, \
            f"Expected total income {total_income}, got {result.total_income}"
        
        print(f"\n✓ Results:")
        print(f"   Total Income: {result.total_income:,.2f} GEL")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        print(f"   Effective Rate: {result.effective_rate * 100:.2f}%")
        print(f"   Regimes: {len(result.by_regime)}")
        
        return result
    
    def scenario_non_resident(self):
        """Scenario: Non-resident with Georgian-source income."""
        print("\n📋 User Profile:")
        print("   - Non-Resident")
        print("   - Salary: 6,000 GEL/month × 12 months")
        print("   - Dividends: 8,000 GEL")
        
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.NON_RESIDENT,
            salary=[
                SalaryIncome(monthly_gross=6000.0, months=12, pension_employee_rate=0.02)
            ],
            dividends=[DividendsIncome(amount=8000.0)]
        )
        
        result = calculate_all(profile)
        
        assert result.residency == ResidencyStatus.NON_RESIDENT, "Should be non-resident"
        
        expected_salary_tax = 6000 * 12 * 0.20  # 14,400
        expected_dividends_tax = 8000 * 0.05  # 400
        expected_total_tax = expected_salary_tax + expected_dividends_tax  # 14,800
        
        assert abs(result.total_tax - expected_total_tax) < 0.01, \
            f"Expected total tax {expected_total_tax}, got {result.total_tax}"
        
        print(f"\n✓ Results:")
        print(f"   Residency: {result.residency.value}")
        print(f"   Total Income: {result.total_income:,.2f} GEL")
        print(f"   Total Tax: {result.total_tax:,.2f} GEL")
        
        return result
    
    def scenario_add_remove_items(self):
        """Scenario: User adds and removes multiple items (simulating UI interactions)."""
        print("\n📋 Simulating UI interactions:")
        print("   1. Add salary source")
        print("   2. Add rental property")
        print("   3. Add dividends")
        print("   4. Remove rental property")
        print("   5. Add capital gains")
        
        # Step 1: Start with salary
        profile = UserProfile(
            year=2025,
            residency=ResidencyStatus.RESIDENT,
            salary=[SalaryIncome(monthly_gross=3000.0, months=12, pension_employee_rate=0.02)]
        )
        result1 = calculate_all(profile)
        assert len(result1.by_regime) == 1, "Should have 1 regime"
        assert "salary" in [r.regime_id for r in result1.by_regime], "Should have salary"
        
        # Step 2: Add rental
        profile.rental.append(RentalIncome(monthly_rent=1000.0, months=12, special_5_percent=True))
        result2 = calculate_all(profile)
        assert len(result2.by_regime) == 2, "Should have 2 regimes"
        assert "rental" in [r.regime_id for r in result2.by_regime], "Should have rental"
        
        # Step 3: Add dividends
        profile.dividends.append(DividendsIncome(amount=5000.0))
        result3 = calculate_all(profile)
        assert len(result3.by_regime) == 3, "Should have 3 regimes"
        assert "dividends" in [r.regime_id for r in result3.by_regime], "Should have dividends"
        
        # Step 4: Remove rental (simulate user removing it)
        profile.rental = []
        result4 = calculate_all(profile)
        assert len(result4.by_regime) == 2, "Should have 2 regimes"
        assert "rental" not in [r.regime_id for r in result4.by_regime], "Should not have rental"
        
        # Step 5: Add capital gains
        profile.capital_gains.append(
            CapitalGainsIncome(purchase_price=100000.0, sale_price=120000.0, is_primary_residence=False)
        )
        result5 = calculate_all(profile)
        assert len(result5.by_regime) == 3, "Should have 3 regimes"
        assert "capital_gains" in [r.regime_id for r in result5.by_regime], "Should have capital gains"
        
        print(f"\n✓ Results:")
        print(f"   Final Total Income: {result5.total_income:,.2f} GEL")
        print(f"   Final Total Tax: {result5.total_tax:,.2f} GEL")
        print(f"   Final Regimes: {len(result5.by_regime)}")
        
        return result5
    
    def scenario_empty_to_full(self):
        """Scenario: User starts with empty profile and builds it up."""
        print("\n📋 Simulating user building profile from scratch:")
        
        # Start empty
        profile = UserProfile(year=2025, residency=ResidencyStatus.RESIDENT)
        result_empty = calculate_all(profile)
        assert result_empty.total_tax == 0.0, "Empty profile should have 0 tax"
        assert result_empty.total_income == 0.0, "Empty profile should have 0 income"
        assert len(result_empty.by_regime) == 0, "Empty profile should have no regimes"
        
        # Add salary
        profile.salary.append(SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02))
        result_salary = calculate_all(profile)
        assert result_salary.total_tax > 0, "Should have tax after adding salary"
        
        # Add rental
        profile.rental.append(RentalIncome(monthly_rent=800.0, months=12, special_5_percent=True))
        result_rental = calculate_all(profile)
        assert result_rental.total_tax > result_salary.total_tax, "Tax should increase after adding rental"
        
        # Add dividends
        profile.dividends.append(DividendsIncome(amount=10000.0))
        result_final = calculate_all(profile)
        assert result_final.total_tax > result_rental.total_tax, "Tax should increase after adding dividends"
        
        print(f"\n✓ Results:")
        print(f"   Empty → Salary: {result_salary.total_tax:,.2f} GEL tax")
        print(f"   + Rental: {result_rental.total_tax:,.2f} GEL tax")
        print(f"   + Dividends: {result_final.total_tax:,.2f} GEL tax")
        print(f"   Final Income: {result_final.total_income:,.2f} GEL")
        
        return result_final
    
    def run_all_scenarios(self):
        """Run all user scenarios."""
        print("\n" + "="*80)
        print("USER SCENARIO TESTS")
        print("="*80)
        
        scenarios = [
            ("Typical Resident", self.scenario_typical_resident),
            ("Small Business Owner", self.scenario_small_business_owner),
            ("Micro Business Eligible", self.scenario_micro_business_eligible),
            ("Property Seller", self.scenario_property_seller),
            ("Complex Multi-Income", self.scenario_complex_multi_income),
            ("Non-Resident", self.scenario_non_resident),
            ("Add/Remove Items", self.scenario_add_remove_items),
            ("Empty to Full Profile", self.scenario_empty_to_full),
        ]
        
        for scenario_name, scenario_func in scenarios:
            self.run_scenario(scenario_name, scenario_func)
        
        print("\n" + "="*80)
        print("SCENARIO SUMMARY")
        print("="*80)
        
        passed = sum(1 for r in self.test_results if r["status"] == "PASSED")
        failed = sum(1 for r in self.test_results if r["status"] == "FAILED")
        total = len(self.test_results)
        
        print(f"Total Scenarios: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed Scenarios:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  - {result['name']}: {result.get('error', 'Unknown error')}")
        
        print("="*80)
        
        return failed == 0


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run user scenario tests for tax calculator")
    parser.add_argument(
        "--scenario",
        type=str,
        help="Run specific scenario by name"
    )
    
    args = parser.parse_args()
    
    tester = UserScenarioTester()
    
    if args.scenario:
        # Run specific scenario
        scenario_method = getattr(tester, f"scenario_{args.scenario.lower().replace(' ', '_')}", None)
        if scenario_method:
            tester.run_scenario(args.scenario, scenario_method)
        else:
            print(f"Scenario '{args.scenario}' not found.")
            print("Available scenarios:")
            for method in dir(tester):
                if method.startswith("scenario_"):
                    print(f"  - {method[9:]}")
    else:
        # Run all scenarios
        success = tester.run_all_scenarios()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

