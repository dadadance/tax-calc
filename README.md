````markdown
# Georgian Personal Tax Calculator – Product Spec & Development Roadmap

Version: 0.1  
Owner: Levan  
Status: Draft for development

---

## 1. Goal

Build a **single-page web application** that calculates Georgian taxes for individuals (residents and non-residents), showing **clear step-by-step calculations**, based on Georgian tax law and RS.ge forms.

- Target users:
  - Individuals living in Georgia with salary, small/micro business, rental income, etc.
  - Non-residents with Georgian-source income.
  - Accountants and consultants who need a quick, visual calculator.
- Positioning:
  - **Unofficial** tool.
  - Focus on **clarity of logic and education**, not on edge-case completeness.
- Design constraint:
  - Entire user experience must be on **one page** (SPA/layout-wise), with collapsible sections.

---

## 2. Scope

### 2.1. In scope (core)

Covered **regimes and income types**:

1. **Salary / employment income**
   - Georgian-source salary.
   - Resident and non-resident.
   - 20% PIT on salary.
   - Employee pension contributions (2%, later possibly 4%).
   - Monthly vs yearly calculations.

2. **Micro business**
   - 0% tax on business income, if conditions met (turnover, prohibited activities, employees).
   - Turnover and basic eligibility checks reflected in warnings.

3. **Small business**
   - Turnover-based tax:
     - 1% up to 500,000 GEL.
     - 3% on portion above 500,000 GEL.
   - Warning about loss of small business status on exceeding threshold.

4. **Fixed taxpayers / fixed income taxpayers**
   - Regimes with fixed or simplified tax amounts (as defined by RS rules).
   - Represent as “fixed-rate/fixed-amount” regimes.

5. **Residential rental income (special 5% regime)**
   - 5% tax on gross rent where special regime is elected.
   - Per-property and total rental calculations.

6. **Capital gains on property/vehicles**
   - 5% on gains (sale minus purchase), basic holding-period handling:
     - Simple cases first (no exemption, or simple exemption logic).
     - Show formula and note about simplification.

7. **Dividends and interest income**
   - 5% final withholding in common cases.
   - Treated as separate income block.

8. **Property tax (individual)**
   - Very high-level:
     - Check if family income exceeds threshold.
     - If above threshold, approximate property tax due based on rules.
     - If below threshold, show “no property tax under threshold” result.
   - Detailed band logic can be phased in later.

9. **Residency vs non-residency**
   - Toggle: Resident / Non-resident.
   - Affects which income is included:
     - Residents → worldwide income.
     - Non-residents → Georgian-source income only.
   - Same core rates for simple cases, but text notes on differences.

### 2.2. Out of scope (v1)

- Complex double-taxation treaty handling and foreign tax credits.
- Corporate taxes, VAT, excise, customs.
- Full automation for every RS.declaration variant.
- User accounts, saving scenarios, historical tracking.
- Multi-language beyond **Georgian + English** (for v1, only these).

---

## 3. Non-functional Requirements

- **Accuracy:**  
  - Config-driven rules with tests against known examples (from RS.ge docs, typical scenarios).
  - The app must show **all calculation steps** and intermediate numbers.

- **Maintainability:**  
  - Law changes handled by updating **config files (YAML/JSON)** and minimal Python code.
  - Separation between core engine and UI.

- **Performance:**  
  - Single-page app, all interactions within 100–300 ms on normal connections.
  - No heavy assets; load < 1 MB where possible.

- **Privacy:**  
  - No login.
  - No persistent storage of exact user inputs server-side.
  - Optional: anonymized analytics using brackets (e.g. salary ranges).

- **Legal:**  
  - Permanent visible disclaimer:  
    - “Unofficial calculator, may be outdated or simplified, not professional tax advice.”
    - Show tax-year and “rules version” on the page.

---

## 4. Architecture and Tech Stack

### 4.1. Overall

- **Backend (Python):**
  - FastAPI application.
  - `tax_core` package: rules engine + regime configuration.
  - Pure functions: `(year, residency, regimes, inputs) -> calculation trace`.

- **Frontend (single page):**
  - Server-rendered HTML via **Jinja2** templates.
  - Interactivity via **HTMX** (HTML attributes, partial updates).
  - Styling via **Tailwind CSS**.

- **Deployment:**
  - Containerized (Docker).
  - Can run on simple VPS or PaaS (e.g. fly.io, Railway, etc.).
  - Nginx or Caddy in front if needed.

### 4.2. Modules

1. `tax_core/`
   - `rules_engine.py` – interpreter for rules DSL.
   - `models.py` – dataclasses / Pydantic models for:
     - `UserProfile`, `IncomeItem`, `RegimeResult`, `CalculationStep`.
   - `loader.py` – load YAML/JSON config for a given year and regime.
   - `validators.py` – input validation rules (turnover > 0, etc.).

2. `tax_rules/`
   - `2024/` – YAML files per regime.
   - `2025/` – YAML files per regime.
   - `rules_version.json` – version metadata.

3. `api/`
   - `main.py` – FastAPI initialization.
   - Routes:
     - `GET /` – render one-page UI.
     - `POST /calculate` – accept JSON with profile and incomes, return calculation trace.
     - `GET /meta` – rules version info.

4. `web/`
   - `templates/index.html.j2` – main one-page layout.
   - `templates/partials/` – HTMX fragments (results, breakdowns).
   - Tailwind configuration and compiled CSS.

5. `tests/`
   - `unit/` – unit tests for rules engine.
   - `integration/` – tests for `/calculate` endpoint with fixture inputs.

---

## 5. Frontend UX Spec (One Pager)

### 5.1. Layout

Use responsive layout with Tailwind.

**Top Header (always visible):**

- Title: “Georgian Tax Calculator”
- Subtitle: “For individuals – unofficial estimation tool”
- Badges:
  - Tax year selector: `2024 | 2025` (defaults to latest).
  - Rules version label: e.g. `v2025.01`.
  - Residency toggle: `Resident / Non-resident`.

**Main content area – three sections (stacked on mobile):**

1. **Profile & Settings (left/column 1)**
   - Residency (toggle).
   - Tax year (dropdown or pill toggle).
   - Currency (GEL fixed, but show label for clarity).
   - Language toggle: `KA / EN`.

2. **Income Inputs (center/column 2)**
   Sections as collapsible cards (accordion):

   - **Salary**
     - Inputs:
       - Monthly gross salary OR annual gross.
       - Months worked (1–12).
       - Pension: On/Off; default 2%.
     - Switch to add multiple employment sources if needed later.

   - **Micro Business**
     - Inputs:
       - Annual turnover.
       - Checkboxes:
         - “No employees”.
         - “Activity allowed for micro regime”.
       - If any condition violated → show warning, but still compute standard PIT as fallback.

   - **Small Business**
     - Inputs:
       - Annual turnover.
       - Checkbox “Registered as small business”.
       - Optional: previous year turnover.

   - **Fixed Taxpayer**
     - Inputs:
       - Category/type (dropdown).
       - Number of taxable units or fixed amount basis.

   - **Rental Income**
     - Inputs:
       - Number of residential properties.
       - For each: monthly rent, number of months rented.
       - Checkbox to apply 5% regime.

   - **Capital Gains (Property/Vehicle)**
     - Inputs per object:
       - Purchase price.
       - Sale price.
       - Purchase date.
       - Sale date.
       - Checkbox: “Primary residence” or other simple exemptions if used.

   - **Dividends and Interest**
     - Inputs:
       - Amount of dividends.
       - Amount of interest.

   - **Property Tax**
     - Inputs:
       - Approximate annual family income.
       - Number of properties and basic characteristics (for later band logic).

3. **Results & Calculation Trace (right/column 3)**

   - **Summary card:**
     - Total tax due (per year).
     - Effective total tax rate.
     - Breakdown by regime (salary, micro, small, rental, etc.).

   - **Tabs / Accordion:**
     - “By income type”
     - “By regime”
     - “Step-by-step”

   - **Step-by-step view:**
     - For each regime:
       - Table:
         - `Line` | `Description` | `Formula` | `Values` | `Result`
       - Example:
         - “Income tax on salary” | `tax = gross_salary * 0.20` | `tax = 3000 * 0.20` | `= 600 GEL`
     - Include optional “See relevant RS form” line with reference.

**Footer (always visible or at bottom):**

- Disclaimers:
  - Unofficial, for estimation only.
  - Laws may change; verify with RS.ge or a tax advisor.
- Last update date.
- Link list: RS.ge main portals and relevant FAQs.

---

## 6. Rules Engine Design

### 6.1. Rule DSL (config format)

Use YAML as primary format.

Basic rule types:

1. `rate` – simple rate on base:
   ```yaml
   - type: rate
     id: salary_pit
     label: "PIT on salary (20%)"
     base_expr: "gross_salary"
     rate: 0.20
     legal_ref: "URL or code ref"
````

2. `threshold` – different logic below/above threshold:

   ```yaml
   - type: threshold
     id: small_business_1_3
     label: "Small business 1%/3% on turnover"
     threshold: 500000
     below:
       type: rate
       base_expr: "turnover"
       rate: 0.01
       label: "1% up to 500,000 GEL"
     above:
       type: composite
       components:
         - type: rate
           base_expr: "min(turnover, 500000)"
           rate: 0.01
         - type: rate
           base_expr: "max(turnover - 500000, 0)"
           rate: 0.03
   ```

3. `composite` – sum of subcomponents.

4. `switch` – switch on condition, e.g. residency:

   ```yaml
   - type: switch
     condition: "residency == 'RESIDENT'"
     if_true:
       # resident rules
     if_false:
       # non-resident rules
   ```

### 6.2. Engine responsibilities

* Parse the tree of rules for a selected regime.
* Evaluate expressions with a context dict:

  * `context = { gross_salary, turnover, residency, months_worked, ... }`.
* For each rule evaluation:

  * Produce `CalculationStep`:

    * `id`
    * `description`
    * `formula_str` (symbolic)
    * `values_str` (with numbers)
    * `result`
    * `legal_ref`
* Aggregate:

  * Per regime total.
  * Overall total.

---

## 7. API Design

### 7.1. Request model

`POST /calculate`

```json
{
  "year": 2025,
  "residency": "RESIDENT",  // or "NON_RESIDENT"
  "profile": {
    "family_income": 65000
  },
  "incomes": {
    "salary": [
      {
        "monthly_gross": 3000,
        "months": 12,
        "pension_employee_rate": 0.02
      }
    ],
    "micro_business": [
      {
        "turnover": 25000,
        "no_employees": true,
        "activity_allowed": true
      }
    ],
    "small_business": [],
    "fixed_taxpayer": [],
    "rental": [
      {
        "monthly_rent": 800,
        "months": 12,
        "special_5_percent": true
      }
    ],
    "capital_gains": [],
    "dividends": [
      {
        "amount": 5000
      }
    ],
    "property_tax": [
      {
        "properties": 2
      }
    ]
  }
}
```

### 7.2. Response model

```json
{
  "year": 2025,
  "rules_version": "2025.01",
  "residency": "RESIDENT",
  "total_tax": 12345.67,
  "effective_rate": 0.23,
  "by_regime": [
    {
      "regime_id": "salary",
      "tax": 7200,
      "steps": [
        {
          "id": "salary_gross",
          "description": "Annual gross salary",
          "formula": "gross = monthly_gross * months",
          "values": "gross = 3000 * 12",
          "result": 36000
        },
        {
          "id": "salary_pit",
          "description": "PIT 20% on salary",
          "formula": "tax = gross * 0.20",
          "values": "tax = 36000 * 0.20",
          "result": 7200
        }
      ]
    },
    {
      "regime_id": "rental",
      "tax": 480,
      "steps": [ ... ]
    }
  ]
}
```

Frontend uses this to render summaries and detailed traces.

---

## 8. Testing and Quality

### 8.1. Unit tests

* For each regime:

  * Fixed test cases in YAML:

    * Inputs.
    * Expected tax per regime.
* Engine tests:

  * YAML → engine → actual vs expected.

### 8.2. Integration tests

* Test `/calculate` endpoint with real-like payloads.
* Assert:

  * HTTP 200.
  * Non-empty `by_regime`.
  * Known scenarios match expected totals.

### 8.3. Manual validation

* Compare outputs with:

  * RS.ge examples where available.
  * Manually computed test cases in a spreadsheet.

---

## 9. Versioning and Law Changes

* Each year’s rules in separate folder: `tax_rules/2025`.
* `rules_version.json` contains:

  * `version` (e.g. `2025.01`).
  * `effective_from`.
  * `changed_regimes`.
* Process when laws change:

  1. Update YAML for impacted regimes.
  2. Append/change tests.
  3. Bump version, run tests.
  4. Deploy.
* UI shows current `rules_version` and change date.

---

## 10. Development Roadmap

### Phase 1 – Foundations (1–2 weeks)

* Set up repo:

  * Python project with FastAPI, uvicorn.
  * `tax_core` module and basic structure.
  * Tailwind pipeline (CLI or PostCSS).
  * Basic Dockerfile.

* Implement:

  * `/` → static HTML “Hello Georgian Tax Calculator”.
  * `/calculate` → dummy implementation (echo back payload).

### Phase 2 – Rules Engine and Salary Regime (1–2 weeks)

* Implement rule DSL and interpreter.
* Add `2025/salary.yaml`.
* Implement:

  * Request/response models.
  * Real `/calculate` logic for salary only.
* Frontend:

  * One-page layout skeleton.
  * Salary card with HTMX and summary + steps.

### Phase 3 – Micro and Small Business (2 weeks)

* Define YAML rules for `micro_business` and `small_business`.
* Implement unit tests for typical turnover scenarios.
* Frontend:

  * Cards for micro/small business inputs.
  * Show warnings when conditions fail (no employees, etc.).
  * Show 1%/3% breakdown clearly.

### Phase 4 – Rental, Dividends, Capital Gains, Property Tax (2–3 weeks)

* Add YAML rules for:

  * rental (5% regime),
  * dividends,
  * basic capital gains,
  * basic property tax.
* Extend `/calculate` to cover all regimes.
* Frontend:

  * Cards for each income type.
  * Step-by-step trace integrated into UI tabs.

### Phase 5 – Residency, Language, Polish (2 weeks)

* Apply residency logic:

  * Filter income sets or apply different rules based on toggle.
* Add Georgian and English translations (static JSON/string maps).
* Polish UI:

  * Tailwind-based layout improvements.
  * Mobile responsiveness.
  * Clear disclaimers and RS links.

### Phase 6 – Stabilization and Documentation (1–2 weeks)

* Performance pass (minimize payloads, cache static assets).
* Hardening:

  * Input validation.
  * Error messages (e.g. “Negative turnover not allowed”).
* Documentation:

  * README and simple admin guide:

    * How to update tax rules.
    * How to add a new regime.
  * Example config and test cases.

---

## 11. Hand-off Summary for Devs

* Implement FastAPI backend + `tax_core` engine + YAML rule config.
* Implement one-page frontend using Jinja + HTMX + Tailwind.
* Build regimes incrementally in this order:

  1. Salary
  2. Micro + Small business
  3. Rental + Dividends
  4. Capital gains + Property tax
* Ensure every regime shows:

  * Formulas.
  * Numerical substitutions.
  * Final totals.
* Keep laws and RS forms **out of code** and in **versioned configs** wherever possible.