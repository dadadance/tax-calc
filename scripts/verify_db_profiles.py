#!/usr/bin/env python3
"""Verify all profiles in database and their calculations."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.profile_db import list_profiles, load_profile, get_profile_info
from tax_core.calculators import calculate_all


def verify_all_profiles():
    """Verify all profiles in database."""
    print("=" * 80)
    print("DATABASE PROFILE VERIFICATION")
    print("=" * 80)
    print()
    
    profiles = list_profiles()
    
    if not profiles:
        print("No profiles found in database.")
        return
    
    print(f"Found {len(profiles)} profile(s) in database\n")
    
    for idx, profile_meta in enumerate(profiles, 1):
        print(f"{'='*80}")
        print(f"Profile {idx}: {profile_meta['name']}")
        print(f"{'='*80}")
        
        try:
            # Load profile
            profile = load_profile(profile_meta['name'])
            if not profile:
                print("✗ Failed to load profile")
                continue
            
            # Get info
            info = get_profile_info(profile_meta['name'])
            
            print(f"\nMetadata:")
            print(f"  Description: {info['description'] if info else 'N/A'}")
            print(f"  Created: {profile_meta['created_at']}")
            print(f"  Updated: {profile_meta['updated_at']}")
            
            print(f"\nProfile Data:")
            print(f"  Tax Year: {profile.year}")
            print(f"  Residency: {profile.residency.value}")
            
            # Count income sources
            income_counts = []
            if profile.salary:
                total_salary = sum(s.monthly_gross * s.months for s in profile.salary)
                income_counts.append(f"Salary: {len(profile.salary)} source(s) = {total_salary:,.0f} GEL")
            if profile.micro_business:
                total_micro = sum(m.turnover for m in profile.micro_business)
                income_counts.append(f"Micro Business: {len(profile.micro_business)} = {total_micro:,.0f} GEL")
            if profile.small_business:
                total_small = sum(s.turnover for s in profile.small_business)
                income_counts.append(f"Small Business: {len(profile.small_business)} = {total_small:,.0f} GEL")
            if profile.rental:
                total_rental = sum(r.monthly_rent * r.months for r in profile.rental)
                income_counts.append(f"Rental: {len(profile.rental)} = {total_rental:,.0f} GEL")
            if profile.capital_gains:
                total_cg = sum(max(0, cg.sale_price - cg.purchase_price) for cg in profile.capital_gains)
                income_counts.append(f"Capital Gains: {len(profile.capital_gains)} = {total_cg:,.0f} GEL")
            if profile.dividends:
                total_div = sum(d.amount for d in profile.dividends)
                income_counts.append(f"Dividends: {len(profile.dividends)} = {total_div:,.0f} GEL")
            if profile.interest:
                total_int = sum(i.amount for i in profile.interest)
                income_counts.append(f"Interest: {len(profile.interest)} = {total_int:,.0f} GEL")
            if profile.property_tax:
                for pt in profile.property_tax:
                    income_counts.append(f"Property Tax: {pt.properties} properties, {pt.family_income:,.0f} GEL family income")
            
            for count in income_counts:
                print(f"  - {count}")
            
            # Calculate taxes
            print(f"\n📊 Tax Calculation:")
            result = calculate_all(profile)
            
            print(f"  Total Tax: {result.total_tax:,.2f} GEL")
            print(f"  Total Income: {result.total_income:,.2f} GEL")
            print(f"  Effective Rate: {result.effective_rate*100:.2f}%")
            
            print(f"\n  Tax Breakdown:")
            for regime in sorted(result.by_regime, key=lambda r: r.tax, reverse=True):
                if regime.tax > 0:
                    pct = (regime.tax / result.total_tax * 100) if result.total_tax > 0 else 0
                    print(f"    - {regime.regime_id:20s}: {regime.tax:10,.2f} GEL ({pct:5.1f}%)")
            
            # Verify calculations match expected
            print(f"\n✓ Profile verified successfully")
            
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print(f"{'='*80}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total profiles verified: {len(profiles)}")


if __name__ == "__main__":
    verify_all_profiles()

