# RS.ge Integration Technical Plan

## Overview

This document outlines the technical plan for integrating RS.ge (Revenue Service of Georgia) data into the Georgian Tax Calculator application. The integration will allow users to import their personal tax data directly from RS.ge or via manual file uploads.

## Research Findings

### RS.ge API Services

1. **Public Web Services**: RS.ge provides public web services at https://services.rs.ge/
2. **API Type**: SOAP-based API (based on RS.ge Waybill integration examples)
3. **Authentication**: Requires RS.ge account credentials and API registration
4. **Documentation**: Technical documentation available (may require registration/contact)

### Available Data Sources

Based on RS.ge taxpayer portal capabilities, the following data can potentially be accessed:

1. **Income Declarations**
   - Annual income statements
   - Monthly income breakdowns
   - Source of income (salary, business, rental, etc.)

2. **Tax Payments History**
   - Payment records
   - Payment dates and amounts
   - Tax types (PIT, property tax, etc.)

3. **Property Information**
   - Registered properties
   - Property assessments
   - Property tax history

4. **Business Registrations**
   - Micro business status
   - Small business status
   - Business turnover records

5. **Previous Tax Returns**
   - Historical tax calculations
   - Declared income by category

### Manual Export Options

Users can manually export data from RS.ge portal in:
- CSV format
- Excel format
- PDF format (may require parsing)

## Architecture

### Module Structure

```
tax_core/
├── rs_ge/
│   ├── __init__.py
│   ├── api_client.py      # RS.ge API client
│   ├── auth.py            # Authentication handling
│   ├── data_mapper.py     # Map RS.ge data to our models
│   └── exceptions.py      # Custom exceptions
├── importers/
│   ├── __init__.py
│   ├── csv_importer.py    # CSV file import
│   ├── excel_importer.py  # Excel file import
│   └── base_importer.py   # Base importer class
```

### Data Flow

```
RS.ge API / Manual Export
    ↓
Authentication / File Upload
    ↓
Data Retrieval / Parsing
    ↓
Data Mapping (RS.ge format → UserProfile)
    ↓
Validation
    ↓
Integration into app.py UI
```

## Implementation Plan

### Phase 1: Research & Documentation ✅

- [x] Research RS.ge API documentation
- [x] Identify available endpoints
- [x] Document authentication requirements
- [x] Create technical plan

### Phase 2: API Integration Module

#### 2.1 Authentication Module (`tax_core/rs_ge/auth.py`)

**Responsibilities:**
- Handle RS.ge account authentication
- Manage API credentials securely
- Token management and refresh
- Session handling

**Key Functions:**
```python
def authenticate(username: str, password: str) -> AuthToken
def refresh_token(token: AuthToken) -> AuthToken
def validate_credentials(credentials: dict) -> bool
```

**Security Considerations:**
- Never store passwords in plain text
- Use environment variables or secure credential storage
- Implement token expiration handling
- Support for 2FA if required by RS.ge

#### 2.2 API Client (`tax_core/rs_ge/api_client.py`)

**Responsibilities:**
- Make API requests to RS.ge services
- Handle SOAP/HTTP requests
- Error handling and retries
- Rate limiting

**Key Functions:**
```python
def get_income_declarations(year: int) -> List[Dict]
def get_tax_payments(year: int) -> List[Dict]
def get_property_info() -> List[Dict]
def get_business_info() -> Dict
```

**Endpoints to Implement:**
- Income declarations endpoint
- Tax payments endpoint
- Property information endpoint
- Business registration endpoint

#### 2.3 Data Mapper (`tax_core/rs_ge/data_mapper.py`)

**Responsibilities:**
- Convert RS.ge API responses to our `UserProfile` model
- Handle data type conversions
- Map income categories
- Handle missing or incomplete data

**Key Functions:**
```python
def map_to_user_profile(rs_data: Dict, year: int) -> UserProfile
def map_salary_income(rs_data: Dict) -> List[SalaryIncome]
def map_business_income(rs_data: Dict) -> Tuple[List[MicroBusinessIncome], List[SmallBusinessIncome]]
def map_property_info(rs_data: Dict) -> List[PropertyTaxInput]
```

**Mapping Rules:**
- RS.ge income categories → Our income types
- Date formats conversion
- Currency handling (GEL)
- Missing data defaults

### Phase 3: Manual Import Feature

#### 3.1 CSV Importer (`tax_core/importers/csv_importer.py`)

**Responsibilities:**
- Parse CSV files exported from RS.ge
- Validate CSV structure
- Extract relevant data fields
- Handle encoding issues

**Key Functions:**
```python
def parse_csv(file_path: str) -> Dict
def validate_csv_structure(csv_data: List[Dict]) -> bool
def extract_income_data(csv_data: List[Dict]) -> UserProfile
```

**Expected CSV Format:**
- Headers: Income Type, Amount, Period, Year, etc.
- Multiple rows for different income sources
- Date formats: YYYY-MM-DD or DD/MM/YYYY

#### 3.2 Excel Importer (`tax_core/importers/excel_importer.py`)

**Responsibilities:**
- Parse Excel files (.xlsx, .xls)
- Handle multiple sheets
- Extract data from specific ranges
- Support different Excel formats

**Key Functions:**
```python
def parse_excel(file_path: str) -> Dict
def read_sheet(sheet_name: str) -> List[Dict]
def extract_income_data(excel_data: Dict) -> UserProfile
```

**Expected Excel Format:**
- Sheet 1: Income declarations
- Sheet 2: Property information (optional)
- Sheet 3: Tax payments (optional)

#### 3.3 Base Importer (`tax_core/importers/base_importer.py`)

**Responsibilities:**
- Common import functionality
- Data validation
- Error handling
- Progress tracking

**Key Functions:**
```python
class BaseImporter:
    def validate(self, data: Any) -> bool
    def import_data(self, source: Any) -> UserProfile
    def get_errors(self) -> List[str]
```

### Phase 4: UI Integration

#### 4.1 Streamlit UI Components

**New UI Elements in `app.py`:**

1. **RS.ge Import Section** (Sidebar or new tab)
   - "Import from RS.ge" button
   - Credential input fields (username, password)
   - Connection status indicator
   - Data preview before import

2. **Manual Import Section**
   - File upload widget (CSV/Excel)
   - File format selector
   - Import preview
   - Validation feedback

3. **Import Results Display**
   - Summary of imported data
   - Mapping confirmation
   - Override options
   - Apply/Cancel buttons

**Key UI Functions:**
```python
def render_rs_ge_import_section()
def render_manual_import_section()
def preview_imported_data(profile: UserProfile)
def apply_imported_data(profile: UserProfile)
```

## Data Mapping Specifications

### RS.ge → UserProfile Mapping

| RS.ge Field | Our Model | Notes |
|------------|-----------|-------|
| Salary/Employment Income | `SalaryIncome` | Monthly/annual conversion |
| Micro Business Turnover | `MicroBusinessIncome` | Check eligibility flags |
| Small Business Turnover | `SmallBusinessIncome` | Check registration status |
| Rental Income | `RentalIncome` | Monthly rent × months |
| Property Sales | `CapitalGainsIncome` | Sale price - purchase price |
| Dividends | `DividendsIncome` | Direct mapping |
| Interest | `InterestIncome` | Direct mapping |
| Property Tax Info | `PropertyTaxInput` | Property values, types |

### Handling Missing Data

- **Missing fields**: Use defaults from `UserProfile` model
- **Invalid data**: Log warnings, skip invalid entries
- **Date parsing errors**: Use current year as fallback
- **Currency**: Assume GEL, warn if other currency detected

## Security & Privacy

### Credential Storage

- **Development**: Environment variables or `.env` file (gitignored)
- **Production**: Secure credential management (e.g., Streamlit secrets)
- **User credentials**: Never stored, only used for API calls

### Data Privacy

- All data processing happens client-side (Streamlit session)
- No data sent to external servers (except RS.ge API)
- User can review all imported data before applying
- Clear data deletion options

### Error Handling

- **API errors**: Graceful degradation, show user-friendly messages
- **Network errors**: Retry logic with exponential backoff
- **Authentication errors**: Clear instructions for user
- **Data validation errors**: Show specific field errors

## Testing Strategy

### Unit Tests

- Test each mapper function with sample RS.ge data
- Test CSV/Excel parsers with various formats
- Test authentication flow
- Test error handling

### Integration Tests

- Test full import flow (API → UserProfile)
- Test manual import flow (File → UserProfile)
- Test UI integration
- Test edge cases (missing data, invalid formats)

### Manual Testing

- Test with real RS.ge account (if available)
- Test with sample CSV/Excel exports
- Test UI/UX flow
- Test error scenarios

## Dependencies

### New Python Packages

```toml
# For RS.ge API (SOAP)
zeep = "^4.2.1"  # SOAP client

# For Excel import
openpyxl = "^3.1.2"  # Excel file reading
pandas = "^2.1.0"  # Data manipulation (if needed)

# For CSV import
csv = "built-in"  # Standard library

# For secure credential storage
python-dotenv = "^1.0.0"  # Environment variables
```

## Implementation Timeline

1. **Week 1**: Research & Technical Plan ✅
2. **Week 2**: API Client & Authentication Module
3. **Week 3**: Data Mapper & Manual Import
4. **Week 4**: UI Integration & Testing
5. **Week 5**: Documentation & Polish

## Known Limitations

1. **API Access**: May require official registration with RS.ge
2. **API Documentation**: May not be publicly available
3. **Data Format**: RS.ge export formats may vary
4. **Rate Limiting**: API may have rate limits
5. **Authentication**: May require 2FA or special permissions

## Next Steps

1. ✅ Complete research and technical plan
2. ⏳ Implement API client module structure
3. ⏳ Implement manual import feature
4. ⏳ Integrate into Streamlit UI
5. ⏳ Test with real data (if available)
6. ⏳ Document usage for end users

## References

- RS.ge Public Web Services: https://services.rs.ge/
- RS.ge Main Portal: https://www.rs.ge/
- RS.ge Taxpayer Portal: https://www.rs.ge/TaxPayer-en
- RS.ge Contact: info@rs.ge, 2 299 299

