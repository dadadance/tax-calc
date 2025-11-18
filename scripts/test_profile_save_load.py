#!/usr/bin/env python3
"""Test script to save example profiles to database and verify calculations."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.example_profiles import EXAMPLE_PROFILES
from tax_core.profile_db import save_profile, load_profile, list_profiles, init_db, get_profile_info
from tax_core.calculators import calculate_all


def test_profile_save_and_calculate():
    """Test saving profiles and verifying calculations."""
    print("=" * 80)
    print("PROFILE SAVE & CALCULATION TEST")
    print("=" * 80)
    print()
    
    # Initialize database
    init_db()
    print("✓ Database initialized")
    print()
    
    # Select 3-4 profiles to test
    test_profiles = [
        ("typical_employee", "Typical Employee - Test"),
        ("high_income_professional", "High Income Professional - Test"),
        ("complex_multi_income", "Complex Multi-Income - Test"),
        ("property_investor", "Property Investor - Test")
    ]
    
    saved_profiles = []
    
    for profile_key, test_name in test_profiles:
        print(f"\n{'='*80}")
        print(f"Processing: {EXAMPLE_PROFILES[profile_key]['name']}")
        print(f"{'='*80}")
        
        # Get original profile
        original_data = EXAMPLE_PROFILES[profile_key]
        profile = original_data["profile"]
        
        # Make some adjustments
        print(f"\nOriginal Profile:")
        print(f"  Year: {profile.year}")
        print(f"  Residency: {profile.residency.value}")
        
        # Adjustments: modify some values slightly
        if profile.salary:
            print(f"  Original Salary: {profile.salary[0].monthly_gross:,.0f} GEL/month")
            # Increase salary by 10%
            profile.salary[0].monthly_gross = profile.salary[0].monthly_gross * 1.1
            print(f"  Adjusted Salary: {profile.salary[0].monthly_gross:,.0f} GEL/month (+10%)")
        
        if profile.property_tax:
            print(f"  Original Family Income: {profile.property_tax[0].family_income:,.0f} GEL")
            # Recalculate family income from all sources
            total_income = 0.0
            for s in profile.salary:
                total_income += s.monthly_gross * s.months
            for m in profile.micro_business:
                total_income += m.turnover
            for s in profile.small_business:
                total_income += s.turnover
            for r in profile.rental:
                total_income += r.monthly_rent * r.months
            for cg in profile.capital_gains:
                if cg.sale_price > cg.purchase_price:
                    total_income += cg.sale_price - cg.purchase_price
            for d in profile.dividends:
                total_income += d.amount
            for i in profile.interest:
                total_income += i.amount
            
            profile.property_tax[0].family_income = total_income
            print(f"  Adjusted Family Income: {profile.property_tax[0].family_income:,.0f} GEL (recalculated)")
        
        # Calculate before saving
        print(f"\n📊 Calculating taxes...")
        result_before = calculate_all(profile)
        print(f"  Total Tax: {result_before.total_tax:,.2f} GEL")
        print(f"  Total Income: {result_before.total_income:,.2f} GEL")
        print(f"  Effective Rate: {result_before.effective_rate*100:.2f}%")
        
        # Save to database
        description = f"{original_data['description']} (Test - Adjusted)"
        try:
            profile_id = save_profile(test_name, profile, description)
            print(f"\n✓ Saved to database (ID: {profile_id})")
            saved_profiles.append((test_name, profile_id))
        except Exception as e:
            print(f"\n✗ Error saving: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    # Verify saved profiles
    print(f"\n\n{'='*80}")
    print("VERIFICATION: Loading from Database")
    print(f"{'='*80}")
    
    all_profiles = list_profiles()
    print(f"\nTotal profiles in database: {len(all_profiles)}")
    
    for profile_name, _ in saved_profiles:
        print(f"\n{'-'*80}")
        print(f"Loading: {profile_name}")
        print(f"{'-'*80}")
        
        try:
            # Load profile
            loaded_profile = load_profile(profile_name)
            if not loaded_profile:
                print(f"✗ Profile not found!")
                continue
            
            # Get info
            info = get_profile_info(profile_name)
            if info:
                print(f"\nProfile Info:")
                print(f"  Name: {info['name']}")
                print(f"  Description: {info['description']}")
                print(f"  Created: {info['created_at']}")
                print(f"  Updated: {info['updated_at']}")
                print(f"\n  Income Sources:")
                summary = info['income_summary']
                if summary['salary_count'] > 0:
                    print(f"    - Salary: {summary['salary_count']}")
                if summary['micro_business_count'] > 0:
                    print(f"    - Micro Business: {summary['micro_business_count']}")
                if summary['small_business_count'] > 0:
                    print(f"    - Small Business: {summary['small_business_count']}")
                if summary['rental_count'] > 0:
                    print(f"    - Rental: {summary['rental_count']}")
                if summary['capital_gains_count'] > 0:
                    print(f"    - Capital Gains: {summary['capital_gains_count']}")
                if summary['dividends_count'] > 0:
                    print(f"    - Dividends: {summary['dividends_count']}")
                if summary['interest_count'] > 0:
                    print(f"    - Interest: {summary['interest_count']}")
                if summary['property_tax_count'] > 0:
                    print(f"    - Property Tax: {summary['property_tax_count']}")
            
            # Calculate taxes
            print(f"\n📊 Calculation Results:")
            result = calculate_all(loaded_profile)
            
            print(f"  Tax Year: {result.year}")
            print(f"  Residency: {result.residency.value}")
            print(f"  Total Tax: {result.total_tax:,.2f} GEL")
            print(f"  Total Income: {result.total_income:,.2f} GEL")
            print(f"  Effective Rate: {result.effective_rate*100:.2f}%")
            
            print(f"\n  Breakdown by Regime:")
            for regime in sorted(result.by_regime, key=lambda r: r.tax, reverse=True):
                if regime.tax > 0:
                    print(f"    - {regime.regime_id}: {regime.tax:,.2f} GEL")
            
            # Show detailed steps for first regime with tax
            for regime in sorted(result.by_regime, key=lambda r: r.tax, reverse=True):
                if regime.tax > 0 and regime.steps:
                    print(f"\n  Detailed Steps ({regime.regime_id}):")
                    for step in regime.steps[:3]:  # Show first 3 steps
                        print(f"    • {step.description}")
                        print(f"      {step.formula} = {step.values}")
                        print(f"      Result: {step.result:,.2f} GEL")
                    if len(regime.steps) > 3:
                        print(f"    ... and {len(regime.steps) - 3} more steps")
                    break
            
            print(f"\n✓ Verification successful!")
            
        except Exception as e:
            print(f"\n✗ Error loading/calculating: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Profiles tested: {len(saved_profiles)}")
    print(f"Profiles in database: {len(all_profiles)}")
    print(f"\n✓ All tests completed!")


if __name__ == "__main__":
    test_profile_save_and_calculate()

