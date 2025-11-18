# Quick Start Guide

## Setup

1. Install dependencies using `uv`:
```bash
uv sync
```

2. Run the Streamlit app:
```bash
uv run streamlit run app.py
```

Or if streamlit is installed globally:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

- **Salary Income**: Calculate PIT (20%) and pension contributions
- **Micro Business**: 0% tax if eligible, with warnings
- **Small Business**: 1% up to 500k GEL, 3% above
- **Rental Income**: 5% special regime or 20% standard
- **Capital Gains**: 5% on gains (with primary residence exemption)
- **Dividends & Interest**: 5% final withholding
- **Property Tax**: Simplified calculation based on family income threshold

## Usage

1. Select tax year and residency status in the sidebar
2. Add income sources using the tabs
3. View results in the "Calculation Results" section
4. Expand "Step-by-Step Calculations" to see detailed breakdowns

## Project Structure

```
tax-calc/
├── app.py                 # Streamlit application
├── tax_core/              # Core calculation logic
│   ├── models.py          # Data models
│   └── calculators.py     # Calculation functions
├── pyproject.toml         # Project dependencies
└── README.md              # Full specification
```

