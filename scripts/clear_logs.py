#!/usr/bin/env python3
"""Script to clear error logs."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.error_logger import logger


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clear error logs")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt"
    )
    
    args = parser.parse_args()
    
    if not args.confirm:
        response = input("Are you sure you want to clear all error logs? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    if logger.clear_logs():
        print("✓ Error logs cleared successfully.")
    else:
        print("✗ Failed to clear error logs. Check permissions.")

if __name__ == "__main__":
    main()

