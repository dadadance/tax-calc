#!/usr/bin/env python3
"""Test script to validate example profiles and show their calculations."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.example_profiles import EXAMPLE_PROFILES, get_example_profile
from tax_core.calculators import calculate_all


def test_all_profiles():
    """Test all example profiles and display results."""
    print("=" * 80)
    print("EXAMPLE PROFILES TEST")
    print("=" * 80)
    print()
    
    for key, data in EXAMPLE_PROFILES.items():
        profile = data["profile"]
        name = data["name"]
        description = data["description"]
        
        print(f"\n{'='*80}")
        print(f"Profile: {name}")
        print(f"Description: {description}")
        print(f"{'='*80}")
        
        # Show profile details
        print(f"\nTax Year: {profile.year}")
        print(f"Residency: {profile.residency.value}")
        
        # Count income sources
        income_sources = []
        if profile.salary:
            income_sources.append(f"{len(profile.salary)} salary source(s)")
        if profile.micro_business:
            income_sources.append(f"{len(profile.micro_business)} micro business(es)")
        if profile.small_business:
            income_sources.append(f"{len(profile.small_business)} small business(es)")
        if profile.rental:
            income_sources.append(f"{len(profile.rental)} rental(s)")
        if profile.capital_gains:
            income_sources.append(f"{len(profile.capital_gains)} capital gain(s)")
        if profile.dividends:
            income_sources.append(f"{len(profile.dividends)} dividend(s)")
        if profile.interest:
            income_sources.append(f"{len(profile.interest)} interest source(s)")
        if profile.property_tax:
            income_sources.append(f"{len(profile.property_tax)} property tax input(s)")
        
        print(f"Income Sources: {', '.join(income_sources) if income_sources else 'None'}")
        
        # Calculate taxes
        try:
            result = calculate_all(profile)
            
            print(f"\n📊 CALCULATION RESULTS:")
            print(f"  Total Tax: {result.total_tax:,.2f} GEL")
            print(f"  Total Income: {result.total_income:,.2f} GEL")
            print(f"  Effective Rate: {result.effective_rate:.2f}%")
            print(f"  Regimes: {len(result.by_regime)}")
            
            all_warnings = []
            if result.by_regime:
                print(f"\n  Breakdown by Regime:")
                for regime in sorted(result.by_regime, key=lambda r: r.tax, reverse=True):
                    if regime.tax > 0:
                        print(f"    - {regime.regime_id}: {regime.tax:,.2f} GEL")
                    if regime.warnings:
                        all_warnings.extend(regime.warnings)
            
            if all_warnings:
                print(f"\n  ⚠️  Warnings ({len(all_warnings)}):")
                for warning in all_warnings[:3]:  # Show first 3
                    print(f"    - {warning}")
                if len(all_warnings) > 3:
                    print(f"    ... and {len(all_warnings) - 3} more")
            
            print("  ✓ Calculation successful")
            
        except Exception as e:
            print(f"  ✗ Calculation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()


def show_profile_summary():
    """Show a summary table of all profiles."""
    print("=" * 80)
    print("EXAMPLE PROFILES SUMMARY")
    print("=" * 80)
    print()
    
    print(f"{'Profile Name':<30} {'Income Types':<30} {'Description'}")
    print("-" * 80)
    
    for key, data in EXAMPLE_PROFILES.items():
        profile = data["profile"]
        name = data["name"]
        description = data["description"][:40] + "..." if len(data["description"]) > 40 else data["description"]
        
        # Count income types
        types = []
        if profile.salary:
            types.append("Salary")
        if profile.micro_business:
            types.append("Micro")
        if profile.small_business:
            types.append("Small")
        if profile.rental:
            types.append("Rental")
        if profile.capital_gains:
            types.append("CG")
        if profile.dividends:
            types.append("Div")
        if profile.interest:
            types.append("Int")
        if profile.property_tax:
            types.append("Prop")
        
        types_str = ", ".join(types) if types else "None"
        
        print(f"{name:<30} {types_str:<30} {description}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test example profiles")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary table only"
    )
    parser.add_argument(
        "--profile",
        type=str,
        help="Test a specific profile by key"
    )
    
    args = parser.parse_args()
    
    if args.summary:
        show_profile_summary()
    elif args.profile:
        if args.profile not in EXAMPLE_PROFILES:
            print(f"Error: Profile '{args.profile}' not found.")
            print(f"Available profiles: {', '.join(EXAMPLE_PROFILES.keys())}")
            sys.exit(1)
        
        data = EXAMPLE_PROFILES[args.profile]
        profile = data["profile"]
        name = data["name"]
        description = data["description"]
        
        print(f"Profile: {name}")
        print(f"Description: {description}")
        print()
        
        result = calculate_all(profile)
        print(f"Total Tax: {result.total_tax:,.2f} GEL")
        print(f"Total Income: {result.total_income:,.2f} GEL")
        print(f"Effective Rate: {result.effective_rate:.2f}%")
    else:
        test_all_profiles()

