# Testing and Scripts Guide

## Overview

This document describes the testing infrastructure and management scripts for the Georgian Tax Calculator application.

## Test Results

✅ **All tests passing!**

**Unit Tests:**
```
Total Tests: 19
Passed: 19
Failed: 0
```

**User Scenario Tests:**
```
Total Scenarios: 8
Passed: 8
Failed: 0
```

## Test Coverage

### Unit Tests (19 tests)

These test individual calculation functions and edge cases:

1. **Salary Calculation** - Basic salary tax calculation
2. **Multiple Salary Sources** - Multiple employment sources
3. **Micro Business Zero Tax** - 0% tax when eligible
4. **Micro Business Fallback** - 20% fallback when conditions not met
5. **Small Business Below Threshold** - 1% rate below 500k GEL
6. **Small Business Threshold** - 1%/3% split above 500k GEL
7. **Rental 5% Regime** - Special 5% rental tax
8. **Rental Standard Rate** - Standard 20% rental tax
9. **Capital Gains** - 5% capital gains tax
10. **Primary Residence Exemption** - Capital gains exemption
11. **Dividends and Interest** - 5% final withholding
12. **Property Tax Below Threshold** - Exemption below income threshold
13. **Non-Resident** - Non-resident tax calculation
14. **Effective Rate Calculation** - Effective tax rate accuracy
15. **Calculation Steps Present** - Step-by-step calculation verification
16. **Warnings Generation** - Warning system functionality
17. **Complex Scenario** - Multi-income type scenarios
18. **Empty Profile** - Edge case handling
19. **Edge Cases** - Zero values, losses, etc.

### User Scenario Tests (8 scenarios)

These test realistic user workflows and end-to-end calculations:

1. **Typical Resident** - Common case: salary + rental + dividends
2. **Small Business Owner** - Business above 500k threshold with part-time salary
3. **Micro Business Eligible** - 0% tax micro business scenario
4. **Property Seller** - Capital gains from property sale
5. **Complex Multi-Income** - Multiple income types (salary, micro, rental, dividends, interest)
6. **Non-Resident** - Non-resident with Georgian-source income
7. **Add/Remove Items** - Simulates UI interactions (adding/removing income sources)
8. **Empty to Full Profile** - Building profile from scratch step by step

## Running Tests

### Run Unit Tests

```bash
# Run all unit tests
uv run python scripts/test_app.py

# Run specific test
uv run python scripts/test_app.py --test salary_calculation
```

### Run User Scenario Tests

```bash
# Run all user scenarios
uv run python scripts/test_user_scenario.py

# Run specific scenario
uv run python scripts/test_user_scenario.py --scenario typical_resident
```

### Test Output

Tests provide:
- ✓/✗ status indicators
- Detailed error messages on failure
- Summary statistics
- Automatic error logging for failures

## Management Scripts

### Start App

```bash
# Start on default port (8501)
uv run python scripts/start_app.py

# Custom port
uv run python scripts/start_app.py --port 8502

# Background mode
uv run python scripts/start_app.py --background

# Headless mode (no browser)
uv run python scripts/start_app.py --headless
```

**Features:**
- Checks if app is already running
- Saves PID for process management
- Provides URL and process information
- Handles port conflicts

### Stop App

```bash
# Normal stop
uv run python scripts/stop_app.py

# Force stop by port
uv run python scripts/stop_app.py --force
```

**Features:**
- Graceful shutdown (SIGTERM)
- Force kill if needed (SIGKILL)
- Port-based kill as fallback
- Cleans up PID file

### View Logs

```bash
# View statistics
uv run python scripts/view_logs.py --stats

# View recent errors
uv run python scripts/view_logs.py -n 10

# View all errors
uv run python scripts/view_logs.py --all

# View specific error
uv run python scripts/view_logs.py --id <error_id>
```

### Clear Logs

```bash
# With confirmation
uv run python scripts/clear_logs.py

# Skip confirmation
uv run python scripts/clear_logs.py --confirm
```

## Complete Workflow

### Development Workflow

1. **Start the app:**
   ```bash
   uv run python scripts/start_app.py
   ```

2. **Run tests:**
   ```bash
   uv run python scripts/test_app.py
   ```

3. **Check for errors:**
   ```bash
   uv run python scripts/view_logs.py --stats
   ```

4. **View recent errors:**
   ```bash
   uv run python scripts/view_logs.py -n 10
   ```

5. **Stop the app:**
   ```bash
   uv run python scripts/stop_app.py
   ```

### CI/CD Workflow

```bash
# Run tests
uv run python scripts/test_app.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
    exit 1
fi
```

## Test Structure

Tests are organized in the `AppTester` class with:
- Individual test methods (`test_*`)
- Error logging for failures
- Assertion-based validation
- Context-aware error messages

## Error Handling

- All test failures are automatically logged
- Errors include full context and stack traces
- Test errors are tracked separately from app errors
- Error logs can be viewed via `view_logs.py`

## Continuous Testing

For continuous testing during development:

```bash
# Watch mode (requires external tool like entr or watchdog)
find . -name "*.py" | entr -c uv run python scripts/test_app.py
```

## Performance

- All 19 tests run in < 1 second
- Tests are isolated and independent
- No external dependencies required
- Can run in parallel (future enhancement)

## Future Enhancements

Potential improvements:
- [ ] Integration tests with actual Streamlit UI
- [ ] Performance benchmarks
- [ ] Load testing
- [ ] Visual regression tests
- [ ] Coverage reports
- [ ] Test data fixtures
- [ ] Mock external dependencies

## Troubleshooting

### Tests Failing?

1. Check error logs: `uv run python scripts/view_logs.py --stats`
2. Run specific test: `uv run python scripts/test_app.py --test <name>`
3. Verify dependencies: `uv sync`
4. Check Python version: Requires Python 3.13+

### App Won't Start?

1. Check if already running: `uv run python scripts/stop_app.py`
2. Check port availability: `lsof -i :8501`
3. Check permissions: Ensure write access to project directory
4. Check logs: `errors/app_errors.log`

### App Won't Stop?

1. Force stop: `uv run python scripts/stop_app.py --force`
2. Manual kill: `kill <pid>` (from PID file)
3. Port-based kill: `lsof -ti :8501 | xargs kill`

## Summary

✅ **19 unit tests** covering all tax regimes and edge cases  
✅ **8 user scenario tests** simulating realistic workflows  
✅ **Automated test execution** with detailed reporting  
✅ **Error logging** for test failures  
✅ **Start/stop scripts** for app management  
✅ **Log viewing tools** for debugging  
✅ **Complete documentation** for all scripts  

The testing infrastructure is complete and ready for continuous development!

### Test Coverage Summary

- **Unit Tests**: Test individual functions and calculations
- **User Scenarios**: Test realistic end-to-end user workflows
- **Total**: 27 test cases covering all aspects of the application

