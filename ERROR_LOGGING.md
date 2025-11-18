# Error Logging System

## Overview

The tax calculator application includes a comprehensive error logging system that captures all errors and exceptions that occur during user interactions. This system helps track issues, debug problems, and monitor application health.

## Features

✅ **Automatic Error Capture** - All errors are automatically logged with full context  
✅ **Structured Logging** - Errors stored in both text and JSON formats  
✅ **Error Tracking** - Unique error IDs for tracking specific issues  
✅ **User Action Context** - Each error includes what the user was doing  
✅ **Full Stack Traces** - Complete traceback information for debugging  
✅ **Statistics & Analytics** - View error counts by type and action  
✅ **Streamlit UI** - Built-in error logs page in the app  
✅ **Command Line Tools** - Scripts for viewing and managing logs  

## Error Log Location

All error logs are stored in the `errors/` directory:

- `errors/app_errors.log` - Human-readable text log file
- `errors/errors.jsonl` - JSON Lines format (one error per line, easy to parse)

The `errors/` directory is automatically created when the app runs.

## Viewing Error Logs

### Option 1: Streamlit UI (Recommended)

1. Run the Streamlit app: `uv run streamlit run app.py`
2. Click "📋 Error Logs" in the sidebar
3. View recent errors, statistics, and filter by type or action

### Option 2: Command Line

```bash
# View last 10 errors
uv run python scripts/view_logs.py

# View statistics
uv run python scripts/view_logs.py --stats

# View specific error
uv run python scripts/view_logs.py --id <error_id>

# View all errors
uv run python scripts/view_logs.py --all
```

### Option 3: Direct File Access

Read the files directly:
- `errors/app_errors.log` - Text format
- `errors/errors.jsonl` - JSON Lines format

## Error Log Structure

Each error log entry contains:

```json
{
  "error_id": "20250101_120000_123456",
  "timestamp": "2025-01-01T12:00:00.123456",
  "error_type": "ValueError",
  "error_message": "Division by zero",
  "user_action": "Calculate Taxes",
  "context": {
    "tax_year": 2025,
    "residency": "RESIDENT",
    "has_salary": true
  },
  "traceback": "Full Python traceback..."
}
```

## Error Categories

Errors are automatically categorized by:

1. **Error Type** - Python exception type (ValueError, KeyError, etc.)
2. **User Action** - What the user was doing (Add Salary, Calculate Taxes, etc.)
3. **Timestamp** - When the error occurred

## Managing Logs

### Clear All Logs

```bash
# With confirmation
uv run python scripts/clear_logs.py

# Skip confirmation
uv run python scripts/clear_logs.py --confirm
```

### Export Logs

From the Streamlit Error Logs page, click "📥 Download Logs as JSON" to export all errors.

## Error Handling in Code

The application uses the `tax_core.error_logger` module for consistent error logging:

```python
from tax_core.error_logger import log_app_error

try:
    # Your code here
    pass
except Exception as e:
    log_app_error(e, user_action="Description of user action", **context)
    # Handle error
```

## Testing

Run automated tests to verify error logging:

```bash
uv run python scripts/test_app.py
```

Test failures are automatically logged to the error system.

## Best Practices

1. **Check logs regularly** - Review error logs to identify patterns
2. **Use error IDs** - Reference specific errors by ID when reporting issues
3. **Clear logs after fixes** - Clear logs after resolving issues to start fresh
4. **Monitor statistics** - Use `--stats` to see error trends
5. **Export before clearing** - Export logs before clearing for record keeping

## Troubleshooting

### Logs not appearing?

- Check that `errors/` directory exists and is writable
- Verify the app has write permissions
- Check console output for logging errors

### Too many errors?

- Use `--stats` to identify common error types
- Filter by user action to find problematic workflows
- Review recent errors to identify patterns

### Need to debug a specific error?

1. Get the error ID from the logs
2. Use `--id <error_id>` to view full details
3. Check the traceback and context information

## Integration

The error logging system is integrated throughout the application:

- ✅ All user interactions (button clicks, form submissions)
- ✅ Calculation errors
- ✅ Data validation errors
- ✅ Profile building errors
- ✅ Automated test failures

All errors are automatically captured without requiring manual intervention.

