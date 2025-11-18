#!/usr/bin/env python3
"""Test complex user scenario: salary, dividends, 2 cars, 1 apartment, 2 houses, rental, interest."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.models import (
    UserProfile,
    ResidencyStatus,
    SalaryIncome,
    DividendsIncome,
    InterestIncome,
    RentalIncome,
    CapitalGainsIncome,
)
from tax_core.calculators import calculate_all


def main():
    """Test complex user scenario."""
    print("=" * 80)
    print("COMPLEX USER SCENARIO")
    print("=" * 80)
    print("\n📋 User Profile:")
    print("   - Resident")
    print("   - Salary: 5,000 GEL/month × 12 months")
    print("   - Dividends: 15,000 GEL")
    print("   - Interest: 3,000 GEL")
    print("   - Rental Income: 1,200 GEL/month × 12 months (5% regime)")
    print("   - Capital Gains:")
    print("     • Car 1: Purchased 20k, Sold 25k")
    print("     • Car 2: Purchased 15k, Sold 18k")
    print("     • Apartment: Purchased 80k, Sold 120k")
    print("     • House 1: Purchased 150k, Sold 180k")
    print("     • House 2: Purchased 200k, Sold 250k (primary residence - exempt)")
    
    profile = UserProfile(
        year=2025,
        residency=ResidencyStatus.RESIDENT,
        salary=[
            SalaryIncome(monthly_gross=5000.0, months=12, pension_employee_rate=0.02)
        ],
        dividends=[DividendsIncome(amount=15000.0)],
        interest=[InterestIncome(amount=3000.0)],
        rental=[
            RentalIncome(monthly_rent=1200.0, months=12, special_5_percent=True)
        ],
        capital_gains=[
            # Car 1
            CapitalGainsIncome(
                purchase_price=20000.0,
                sale_price=25000.0,
                is_primary_residence=False
            ),
            # Car 2
            CapitalGainsIncome(
                purchase_price=15000.0,
                sale_price=18000.0,
                is_primary_residence=False
            ),
            # Apartment
            CapitalGainsIncome(
                purchase_price=80000.0,
                sale_price=120000.0,
                is_primary_residence=False
            ),
            # House 1
            CapitalGainsIncome(
                purchase_price=150000.0,
                sale_price=180000.0,
                is_primary_residence=False
            ),
            # House 2 (primary residence - exempt)
            CapitalGainsIncome(
                purchase_price=200000.0,
                sale_price=250000.0,
                is_primary_residence=True  # Exempt!
            ),
        ]
    )
    
    result = calculate_all(profile)
    
    print("\n" + "=" * 80)
    print("CALCULATION RESULTS")
    print("=" * 80)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   Total Income: {result.total_income:,.2f} GEL")
    print(f"   Total Tax Due: {result.total_tax:,.2f} GEL")
    print(f"   Effective Tax Rate: {result.effective_rate * 100:.2f}%")
    
    # Breakdown by regime
    print(f"\n📋 BREAKDOWN BY REGIME:")
    print(f"   {'Regime':<25} {'Tax (GEL)':>15} {'% of Total':>15}")
    print(f"   {'-' * 25} {'-' * 15} {'-' * 15}")
    
    for regime in result.by_regime:
        percentage = (regime.tax / result.total_tax * 100) if result.total_tax > 0 else 0
        regime_name = regime.regime_id.replace("_", " ").title()
        print(f"   {regime_name:<25} {regime.tax:>15,.2f} {percentage:>14.1f}%")
    
    # Detailed breakdown
    print(f"\n📝 DETAILED BREAKDOWN:")
    
    for regime in result.by_regime:
        print(f"\n   {regime.regime_id.replace('_', ' ').title()}:")
        print(f"   {'-' * 60}")
        
        if regime.regime_id == "salary":
            print(f"   • Annual Gross Salary: 60,000 GEL")
            print(f"   • PIT (20%): {regime.tax:,.2f} GEL")
            
        elif regime.regime_id == "dividends":
            print(f"   • Dividends Received: 15,000 GEL")
            print(f"   • Tax (5%): {regime.tax:,.2f} GEL")
            
        elif regime.regime_id == "interest":
            print(f"   • Interest Received: 3,000 GEL")
            print(f"   • Tax (5%): {regime.tax:,.2f} GEL")
            
        elif regime.regime_id == "rental":
            print(f"   • Annual Rental Income: 14,400 GEL")
            print(f"   • Tax (5% special regime): {regime.tax:,.2f} GEL")
            
        elif regime.regime_id == "capital_gains":
            print(f"   • Capital Gains Breakdown:")
            total_gain = 0
            taxable_gain = 0
            
            # Calculate gains
            gains = [
                ("Car 1", 25000 - 20000, False),
                ("Car 2", 18000 - 15000, False),
                ("Apartment", 120000 - 80000, False),
                ("House 1", 180000 - 150000, False),
                ("House 2", 250000 - 200000, True),  # Primary residence
            ]
            
            for name, gain, is_exempt in gains:
                total_gain += gain
                if not is_exempt:
                    taxable_gain += gain
                    tax_on_gain = gain * 0.05
                    print(f"     - {name}: {gain:,.0f} GEL gain → {tax_on_gain:,.2f} GEL tax (5%)")
                else:
                    print(f"     - {name}: {gain:,.0f} GEL gain → EXEMPT (primary residence)")
            
            print(f"   • Total Capital Gains: {total_gain:,.2f} GEL")
            print(f"   • Taxable Gains: {taxable_gain:,.2f} GEL")
            print(f"   • Capital Gains Tax (5%): {regime.tax:,.2f} GEL")
        
        # Show warnings if any
        if regime.warnings:
            print(f"   ⚠️  Warnings:")
            for warning in regime.warnings:
                print(f"      • {warning}")
    
    # Step-by-step view (sample)
    print(f"\n🔍 STEP-BY-STEP CALCULATIONS (Sample):")
    print(f"   {'-' * 60}")
    
    # Show first regime's steps as example
    if result.by_regime:
        first_regime = result.by_regime[0]
        print(f"\n   {first_regime.regime_id.replace('_', ' ').title()}:")
        for i, step in enumerate(first_regime.steps[:3], 1):  # Show first 3 steps
            print(f"   {i}. {step.description}")
            print(f"      Formula: {step.formula}")
            print(f"      Calculation: {step.values}")
            print(f"      Result: {step.result:,.2f} GEL")
            if step.legal_ref:
                print(f"      Reference: {step.legal_ref}")
            print()
    
    print("=" * 80)
    print("\n💡 In the Streamlit app, users would see:")
    print("   1. Summary cards at the top (Total Tax, Total Income, Effective Rate)")
    print("   2. Breakdown table by regime")
    print("   3. Expandable sections for each regime with step-by-step calculations")
    print("   4. Warnings if any (e.g., threshold exceeded)")
    print("   5. Legal references for each calculation step")
    print("=" * 80)


if __name__ == "__main__":
    main()

