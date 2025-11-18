#!/usr/bin/env python3
"""Script to view error logs."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tax_core.error_logger import logger
import json
from datetime import datetime


def format_error(error_data: dict) -> str:
    """Format error data for display."""
    lines = []
    lines.append(f"Error ID: {error_data.get('error_id', 'N/A')}")
    lines.append(f"Timestamp: {error_data.get('timestamp', 'N/A')}")
    lines.append(f"Type: {error_data.get('error_type', 'N/A')}")
    lines.append(f"Message: {error_data.get('error_message', 'N/A')}")
    lines.append(f"User Action: {error_data.get('user_action', 'N/A')}")
    
    context = error_data.get('context', {})
    if context:
        lines.append(f"Context: {json.dumps(context, indent=2, default=str)}")
    
    traceback = error_data.get('traceback', '')
    if traceback:
        lines.append(f"\nTraceback:\n{traceback}")
    
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="View error logs")
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=10,
        help="Number of recent errors to show (default: 10)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show error statistics"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all errors"
    )
    parser.add_argument(
        "--id",
        type=str,
        help="Show specific error by ID"
    )
    
    args = parser.parse_args()
    
    if args.stats:
        stats = logger.get_log_stats()
        print("\n" + "=" * 80)
        print("ERROR STATISTICS")
        print("=" * 80)
        print(f"Total Errors: {stats['total_errors']}")
        print(f"\nErrors by Type:")
        for error_type, count in sorted(stats['errors_by_type'].items(), key=lambda x: -x[1]):
            print(f"  {error_type}: {count}")
        print(f"\nErrors by Action:")
        for action, count in sorted(stats['errors_by_action'].items(), key=lambda x: -x[1]):
            print(f"  {action}: {count}")
        if stats['latest_error']:
            print(f"\nLatest Error:")
            print(f"  ID: {stats['latest_error'].get('error_id')}")
            print(f"  Type: {stats['latest_error'].get('error_type')}")
            print(f"  Time: {stats['latest_error'].get('timestamp')}")
        print("=" * 80 + "\n")
        return
    
    limit = None if args.all else args.number
    
    if args.id:
        errors = logger.get_recent_errors(limit=10000)
        found = [e for e in errors if e.get('error_id') == args.id]
        if found:
            print(format_error(found[0]))
        else:
            print(f"Error with ID '{args.id}' not found.")
        return
    
    errors = logger.get_recent_errors(limit=limit or 10000)
    
    if not errors:
        print("No errors found in logs.")
        return
    
    print(f"\nShowing {len(errors)} error(s):\n")
    
    for i, error_data in enumerate(errors, 1):
        print(f"[{i}/{len(errors)}]")
        print(format_error(error_data))
        print()


if __name__ == "__main__":
    main()

