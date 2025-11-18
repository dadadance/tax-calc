#!/usr/bin/env python3
"""Setup script to initialize the database for new users."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.profile_db import init_db, DB_PATH


def main():
    """Initialize the database."""
    print("=" * 80)
    print("Tax Calculator - Database Setup")
    print("=" * 80)
    print()
    
    try:
        init_db()
        print(f"✓ Database initialized successfully at: {DB_PATH}")
        print(f"✓ Database directory created: {DB_PATH.parent}")
        print()
        print("The database is ready to save and load user profiles.")
        print()
        print("You can now:")
        print("  - Save profiles from the Streamlit app")
        print("  - Load saved profiles")
        print("  - Manage profiles from the UI")
        return 0
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

