# Scripts Documentation

This directory contains utility scripts for managing and testing the tax calculator application.

## Available Scripts

### 1. `start_app.py` - Start the Application

Start the Streamlit tax calculator app.

**Usage:**
```bash
# Start on default port (8501)
uv run python scripts/start_app.py

# Start on custom port
uv run python scripts/start_app.py --port 8502

# Start in headless mode (no browser)
uv run python scripts/start_app.py --headless

# Start in background
uv run python scripts/start_app.py --background
```

**Examples:**
```bash
# Start normally
uv run python scripts/start_app.py

# Start on port 9000
uv run python scripts/start_app.py -p 9000

# Start in background (detached)
uv run python scripts/start_app.py --background
```

**Features:**
- Checks if app is already running
- Saves PID file for process management
- Provides URL and PID information
- Can run in foreground or background mode

### 2. `stop_app.py` - Stop the Application

Stop the running Streamlit app.

**Usage:**
```bash
# Stop the app
uv run python scripts/stop_app.py

# Force kill by port (if PID file missing)
uv run python scripts/stop_app.py --force
```

**Examples:**
```bash
# Normal stop
uv run python scripts/stop_app.py

# Force stop (kills by port)
uv run python scripts/stop_app.py --force --port 8501
```

**Features:**
- Graceful shutdown (SIGTERM)
- Force kill if needed (SIGKILL)
- Port-based kill as fallback
- Cleans up PID file

### 3. `view_logs.py` - View Error Logs

View and analyze error logs from the application.

**Usage:**
```bash
# View last 10 errors (default)
uv run python scripts/view_logs.py

# View last N errors
uv run python scripts/view_logs.py -n 20

# View all errors
uv run python scripts/view_logs.py --all

# Show error statistics
uv run python scripts/view_logs.py --stats

# View specific error by ID
uv run python scripts/view_logs.py --id 20250101_120000_123456
```

**Examples:**
```bash
# Quick stats
uv run python scripts/view_logs.py --stats

# See last 5 errors
uv run python scripts/view_logs.py -n 5
```

### 4. `clear_logs.py` - Clear Error Logs

Clear all error log files.

**Usage:**
```bash
# With confirmation prompt
uv run python scripts/clear_logs.py

# Skip confirmation
uv run python scripts/clear_logs.py --confirm
```

**Warning:** This will permanently delete all error logs. Use with caution.

### 5. `test_app.py` - Unit Tests

Run automated unit tests to verify the calculation engine functionality.

**Usage:**
```bash
# Run all tests
uv run python scripts/test_app.py

# Run specific test
uv run python scripts/test_app.py --test "salary_calculation"
```

**Available Tests (19 total):**
- `salary_calculation` - Test salary tax calculation
- `multiple_salary_sources` - Test multiple salary sources
- `micro_business_zero_tax` - Test micro business 0% tax
- `micro_business_fallback` - Test micro business fallback to 20%
- `small_business_below_threshold` - Test small business below 500k
- `small_business_threshold` - Test small business above 500k threshold
- `rental_5_percent` - Test rental 5% regime
- `rental_standard_rate` - Test rental standard 20% rate
- `capital_gains` - Test capital gains calculation
- `primary_residence_exemption` - Test primary residence exemption
- `dividends_and_interest` - Test dividends and interest
- `property_tax_below_threshold` - Test property tax below threshold
- `non_resident` - Test non-resident calculation
- `effective_rate_calculation` - Test effective tax rate
- `calculation_steps_present` - Test calculation steps
- `warnings_generation` - Test warning generation
- `complex_scenario` - Test complex multi-income scenario
- `empty_profile` - Test empty profile handling
- `edge_cases` - Test edge cases and error handling

**Examples:**
```bash
# Run all tests
uv run python scripts/test_app.py

# Test just salary calculations
uv run python scripts/test_app.py --test salary_calculation

# Test edge cases
uv run python scripts/test_app.py --test edge_cases
```

### 6. `test_user_scenario.py` - User Scenario Tests

Run realistic user scenario tests that simulate actual user workflows.

**Usage:**
```bash
# Run all user scenarios
uv run python scripts/test_user_scenario.py

# Run specific scenario
uv run python scripts/test_user_scenario.py --scenario "typical_resident"
```

**Available Scenarios (8 total):**
- `typical_resident` - Resident with salary, rental, dividends
- `small_business_owner` - Small business owner above threshold
- `micro_business_eligible` - Micro business with 0% tax
- `property_seller` - Property sale with capital gains
- `complex_multi_income` - Multiple income types
- `non_resident` - Non-resident with Georgian income
- `add_remove_items` - Simulates adding/removing income sources
- `empty_to_full` - Building profile from scratch

**Examples:**
```bash
# Run all scenarios
uv run python scripts/test_user_scenario.py

# Test typical resident scenario
uv run python scripts/test_user_scenario.py --scenario typical_resident
```

**What it tests:**
- Realistic user profiles and workflows
- End-to-end calculation accuracy
- Multiple income type combinations
- UI interaction simulation (add/remove items)
- Profile building from empty to full

**Usage:**
```bash
# Run all tests
uv run python scripts/test_app.py

# Run specific test
uv run python scripts/test_app.py --test "salary_calculation"
```

**Available Tests (19 total):**
- `salary_calculation` - Test salary tax calculation
- `multiple_salary_sources` - Test multiple salary sources
- `micro_business_zero_tax` - Test micro business 0% tax
- `micro_business_fallback` - Test micro business fallback to 20%
- `small_business_below_threshold` - Test small business below 500k
- `small_business_threshold` - Test small business above 500k threshold
- `rental_5_percent` - Test rental 5% regime
- `rental_standard_rate` - Test rental standard 20% rate
- `capital_gains` - Test capital gains calculation
- `primary_residence_exemption` - Test primary residence exemption
- `dividends_and_interest` - Test dividends and interest
- `property_tax_below_threshold` - Test property tax below threshold
- `non_resident` - Test non-resident calculation
- `effective_rate_calculation` - Test effective tax rate
- `calculation_steps_present` - Test calculation steps
- `warnings_generation` - Test warning generation
- `complex_scenario` - Test complex multi-income scenario
- `empty_profile` - Test empty profile handling
- `edge_cases` - Test edge cases and error handling

**Examples:**
```bash
# Run all tests
uv run python scripts/test_app.py

# Test just salary calculations
uv run python scripts/test_app.py --test salary_calculation

# Test edge cases
uv run python scripts/test_app.py --test edge_cases
```

## Quick Start Workflow

### Starting the App

```bash
# Start the app
uv run python scripts/start_app.py

# App will be available at http://localhost:8501
```

### Running Tests

```bash
# Run unit tests (19 tests)
uv run python scripts/test_app.py

# Run user scenario tests (8 scenarios)
uv run python scripts/test_user_scenario.py

# Check test results
# All tests should pass
```

### Checking Logs

```bash
# View error statistics
uv run python scripts/view_logs.py --stats

# View recent errors
uv run python scripts/view_logs.py -n 10
```

### Stopping the App

```bash
# Stop the app
uv run python scripts/stop_app.py
```

## Error Logs Location

Error logs are stored in the `errors/` directory:
- `errors/app_errors.log` - Text format log file
- `errors/errors.jsonl` - JSON Lines format (one error per line)

## Process Management

The start/stop scripts use a PID file (`.streamlit.pid`) to track the running process:
- Created when app starts
- Removed when app stops
- Used to check if app is running
- Allows graceful shutdown

## Integration with Streamlit App

The Streamlit app automatically logs errors when they occur. You can view them:
1. In the Streamlit app: Navigate to the "Error Logs" page in the sidebar
2. Via command line: Use `view_logs.py` script
3. Directly: Read the files in `errors/` directory

## Testing Workflow

Recommended workflow for testing:

1. **Start the app:**
   ```bash
   uv run python scripts/start_app.py
   ```

2. **Run automated tests:**
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

## Notes

- All scripts use the `tax_core.error_logger` module for consistent error handling
- Scripts are executable (chmod +x) but can also be run with `python` or `uv run python`
- Error logs are automatically created when the app runs
- The test script logs any test failures to the error log system
- PID file is stored in project root as `.streamlit.pid`
