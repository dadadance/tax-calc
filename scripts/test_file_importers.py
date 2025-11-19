"""Test CSV and Excel importers."""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.importers import CSVImporter, ExcelImporter
from tax_core.models import ResidencyStatus
import tempfile


def create_test_csv():
    """Create a test CSV file."""
    csv_content = """income_type,amount,period,months,description
Salary,120000,annual,12,Monthly salary
Micro Business,50000,annual,12,Micro business turnover
Rental Income,6000,annual,12,Monthly rent 500 GEL
Dividends,5000,annual,1,Dividend income
Interest,2000,annual,1,Interest income
Property,65000,annual,1,Property value"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(csv_content)
        return f.name


def test_csv_importer():
    """Test CSV importer."""
    print("Testing CSV Importer...")
    print("-" * 50)
    
    csv_file = create_test_csv()
    
    try:
        importer = CSVImporter()
        result = importer.import_data(csv_file, 2025)
        
        if result.success:
            print("✓ CSV import successful!")
            profile = result.profile
            
            print(f"\nImported Profile Summary:")
            print(f"  Tax Year: {profile.year}")
            print(f"  Residency: {profile.residency.value}")
            print(f"  Family Income: {profile.family_income:,.2f} GEL")
            print(f"\nIncome Sources:")
            print(f"  Salary: {len(profile.salary)} source(s)")
            print(f"  Micro Business: {len(profile.micro_business)} source(s)")
            print(f"  Small Business: {len(profile.small_business)} source(s)")
            print(f"  Rental: {len(profile.rental)} source(s)")
            print(f"  Dividends: {len(profile.dividends)} source(s)")
            print(f"  Interest: {len(profile.interest)} source(s)")
            print(f"  Property Tax: {len(profile.property_tax)} source(s)")
            
            if result.warnings:
                print(f"\n⚠️ Warnings ({len(result.warnings)}):")
                for warning in result.warnings:
                    print(f"  - {warning}")
            
            if result.errors:
                print(f"\n❌ Errors ({len(result.errors)}):")
                for error in result.errors:
                    print(f"  - {error}")
            
            return True
        else:
            print("❌ CSV import failed!")
            if result.errors:
                for error in result.errors:
                    print(f"  - {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CSV importer: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if os.path.exists(csv_file):
            os.unlink(csv_file)


def create_test_excel():
    """Create a test Excel file."""
    import pandas as pd
    
    data = {
        'income_type': ['Salary', 'Micro Business', 'Rental Income', 'Dividends', 'Interest'],
        'amount': [120000, 50000, 6000, 5000, 2000],
        'period': ['annual', 'annual', 'annual', 'annual', 'annual'],
        'months': [12, 12, 12, 1, 1],
        'description': ['Monthly salary', 'Micro business turnover', 'Monthly rent', 'Dividend income', 'Interest income']
    }
    
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df.to_excel(f.name, index=False, sheet_name='Income')
        return f.name


def test_excel_importer():
    """Test Excel importer."""
    print("\nTesting Excel Importer...")
    print("-" * 50)
    
    excel_file = create_test_excel()
    
    try:
        importer = ExcelImporter()
        result = importer.import_data(excel_file, 2025)
        
        if result.success:
            print("✓ Excel import successful!")
            profile = result.profile
            
            print(f"\nImported Profile Summary:")
            print(f"  Tax Year: {profile.year}")
            print(f"  Residency: {profile.residency.value}")
            print(f"  Family Income: {profile.family_income:,.2f} GEL")
            print(f"\nIncome Sources:")
            print(f"  Salary: {len(profile.salary)} source(s)")
            print(f"  Micro Business: {len(profile.micro_business)} source(s)")
            print(f"  Small Business: {len(profile.small_business)} source(s)")
            print(f"  Rental: {len(profile.rental)} source(s)")
            print(f"  Dividends: {len(profile.dividends)} source(s)")
            print(f"  Interest: {len(profile.interest)} source(s)")
            
            if result.warnings:
                print(f"\n⚠️ Warnings ({len(result.warnings)}):")
                for warning in result.warnings:
                    print(f"  - {warning}")
            
            if result.errors:
                print(f"\n❌ Errors ({len(result.errors)}):")
                for error in result.errors:
                    print(f"  - {error}")
            
            return True
        else:
            print("❌ Excel import failed!")
            if result.errors:
                for error in result.errors:
                    print(f"  - {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Excel importer: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if os.path.exists(excel_file):
            os.unlink(excel_file)


def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing File Importers")
    print("=" * 50)
    
    csv_ok = test_csv_importer()
    excel_ok = test_excel_importer()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"  CSV Importer: {'✓ PASS' if csv_ok else '❌ FAIL'}")
    print(f"  Excel Importer: {'✓ PASS' if excel_ok else '❌ FAIL'}")
    print("=" * 50)
    
    return csv_ok and excel_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

