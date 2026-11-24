# SENTINEL – Fraud Detection Feature Pipeline

## 1. Project Overview

SENTINEL is a fraud detection data-processing project focused on data quality analysis, feature engineering, feature validation, and transaction reason-code generation.

The project uses transaction and related datasets to calculate fraud-related features using historical information available before each transaction.

## 2. Project Objectives

1. Perform data quality analysis.
2. Recompute six transaction features.
3. Compare computed features against the client-provided feature table.
4. Generate transaction reason codes using available rules.
5. Document validation results, mismatches, and implementation limitations.

## 3. Project Structure

```text
sentinel-feature-pipeline/
│
├── data/
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   └── 03_feature_engineering.ipynb
│
├── output/
├── reports/
│
├── src/
│   ├── data_loader.py
│   └── data_quality.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## 4. Prerequisites

The following software and services are required:

- Python
- Git
- Supabase project access
- VS Code or Jupyter Notebook

## 5. Installation Instructions

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd sentinel-feature-pipeline
```

Replace the repository URL with the actual GitHub repository URL.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project uses the following Python libraries:

| Library       | Purpose                                   |
| ------------- | ----------------------------------------- |
| supabase      | Connect to Supabase and retrieve datasets |
| python-dotenv | Load environment variables                |
| pandas        | Data manipulation and analysis            |
| numpy         | Numerical calculations                    |
| matplotlib    | Data visualization                        |
| seaborn       | Statistical visualization and boxplots    |

## 6. Environment Variables Setup

The project uses Supabase credentials to retrieve the required datasets.

### Step 1: Create the Environment File

Create a `.env` file in the project root directory.

### Step 2: Configure Supabase Credentials

Add the following variables:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key
```

Replace the placeholder values with your actual Supabase credentials.

### Step 3: Use the Example Configuration

The repository includes `.env.example`, which provides the required environment variable names without exposing actual credentials.

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Then update `.env` with your actual Supabase credentials.

### Step 4: Secure Credential Handling

- Actual credentials are stored in `.env`.
- The `.env` file is excluded from Git using `.gitignore`.
- `.env.example` contains placeholder values only.
- Actual API keys and credentials must never be committed to GitHub.

The data loader reads environment variables from the project root:

```python
load_dotenv(BASE_DIR / ".env")
```

## 7. Running the Project

### Data Loading

The project provides `main.py` as the data-loading entry point.

Run:

```powershell
python main.py
```

This executes the Supabase data loader, retrieves the configured datasets, and saves the raw datasets as:

```text
output/raw_data.pkl
```

### Notebook Execution

Open the notebooks using VS Code or Jupyter Notebook.

Execute them in the following order:

1. `01_data_loading.ipynb` – Data loading.
2. `02_data_quality_analysis.ipynb` – Data quality analysis.
3. `03_feature_engineering.ipynb` – Feature engineering, validation, and reason-code generation.

Select the project's `.venv` Python interpreter as the notebook kernel.

## 8. Dataset

The project uses the SENTINEL synthetic dataset containing:

- 110,000 transactions
- Customer records
- Merchant records
- Device records
- Payment outcome records
- Label records
- Client-provided feature records

The data loader retrieves the configured tables from Supabase.

## 9. Features Recomputed

The following six features were recomputed:

1. `amount_to_avg_ratio`
2. `is_new_device`
3. `customer_merchant_distance_km`
4. `is_night`
5. `transaction_count_last_1_hour`
6. `transaction_amount_last_24_hours`

Historical calculations use prior transaction data to avoid future data leakage.

## 10. Feature Validation Results

Computed features were compared against the client-provided feature table.

| Feature                          | Exact Match Rate | Numeric Tolerance Match Rate |
| -------------------------------- | ---------------: | ---------------------------: |
| amount_to_avg_ratio              |            2.58% |                       24.08% |
| is_new_device                    |          100.00% |                      100.00% |
| customer_merchant_distance_km    |            8.90% |                       98.63% |
| is_night                         |          100.00% |                      100.00% |
| transaction_count_last_1_hour    |           42.72% |                       42.72% |
| transaction_amount_last_24_hours |           45.74% |                       45.74% |

### Understanding the Match Rates

**Exact Match Rate**

Measures the percentage of records where computed and reference values are exactly equal. Missing values are treated as matching when both sides are missing.

**Numeric Tolerance Match Rate**

Uses NumPy `isclose` with:

- Relative tolerance (`rtol`): `1e-5`
- Absolute tolerance (`atol`): `1e-8`
- Equal missing values: `True`

This comparison allows small floating-point differences.

Tolerance matching is applicable to numeric features.

### Validation Observations

- `is_new_device` and `is_night` achieved 100% exact match rates.
- `customer_merchant_distance_km` improved from 8.90% exact matching to 98.63% tolerance matching.
- `amount_to_avg_ratio` achieved 24.08% tolerance matching.
- Transaction count and transaction amount features showed identical exact and tolerance match rates.

These results indicate that some computed feature definitions or calculation details may differ from the reference implementation. Further investigation and clarification of the reference logic are required.

## 11. Reason-Code Generation

The following four reason codes were implemented using the available definitions and calculations:

| Code | Description     | Transactions Flagged |
| ---- | --------------- | -------------------: |
| R01  | NEW_DEVICE      |                7,305 |
| R03  | ODD_HOUR        |               15,438 |
| R04  | FAILED_ATTEMPTS |                9,877 |
| R06  | NEW_ACCOUNT     |                1,109 |

The following reason codes remain pending because their required rule definitions or thresholds were not available:

- R02 – GEO_MISMATCH
- R05 – AMOUNT_SPIKE
- R07 – VELOCITY
- R08 – HIGH_RISK_MCC

No arbitrary thresholds were introduced.

## 12. Output File

The final reason-code output is:

`sentinel_reason_codes_output.csv`

Output details:

- Total transactions: 110,000
- Output columns: `transaction_id`, `reason_codes`
- A transaction can contain multiple reason codes.
- Transactions without an assigned reason code are marked `NO_REASON_CODE`.

## 13. Important Implementation Notes

- Historical feature calculations use only preceding transaction data.
- Night-time transactions are identified using Indian Standard Time (IST), from 00:00 to before 05:00.
- Distance is calculated using the Haversine formula.
- Missing or unavailable rule definitions are documented rather than replaced with guessed values.
- Feature validation results are documented separately for exact and numeric tolerance matching.

## 14. Conclusion

The SENTINEL feature pipeline recomputes six transaction features, validates them against the client-provided feature table, and generates reason-code output for 110,000 transactions.

Four reason codes are currently implemented. The remaining four require clarification of their rule definitions or thresholds before implementation.

The project also provides documented environment configuration and installation instructions to support reproducible setup.
