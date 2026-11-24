# SENTINEL – Fraud Detection Feature Pipeline

## Project Overview

SENTINEL is a fraud detection data-processing project focused on data quality analysis, feature engineering, feature validation, and transaction reason-code generation.

The project uses transaction and related datasets to calculate fraud-related features using historical information available before each transaction.

## Project Objectives

1. Perform data quality analysis.
2. Recompute six transaction features.
3. Compare computed features against the client-provided feature table.
4. Generate transaction reason codes using available rules.
5. Document results and limitations.

## Dataset

The project uses the SENTINEL synthetic dataset containing 110,000 transactions and related customer, merchant, device, payment outcome, label, and feature records.

## Project Notebooks

| Notebook | Purpose |
|---|---|
| `02_data_quality_analysis.ipynb` | Data quality analysis |
| `03_feature_engineering.ipynb` | Feature engineering, validation and reason-code generation |

## Features Recomputed

The following six features were recomputed:

1. `amount_to_avg_ratio`
2. `is_new_device`
3. `customer_merchant_distance_km`
4. `is_night`
5. `transaction_count_last_1_hour`
6. `transaction_amount_last_24_hours`

Historical calculations use prior transaction data to avoid future data leakage.

## Feature Validation Results

Computed features were compared with the client-provided feature table.

| Feature | Exact Match Rate | Numeric Tolerance Match Rate |
|---|---:|---:|
| amount_to_avg_ratio | 2.58% | 24.08% |
| is_new_device | 100.00% | 100.00% |
| customer_merchant_distance_km | 8.90% | 98.63% |
| is_night | 100.00% | 100.00% |
| transaction_count_last_1_hour | 42.72% | 42.72% |
| transaction_amount_last_24_hours | 45.74% | 45.74% |

Numeric tolerance matching is applicable to numeric features. The match rates indicate that some computed feature definitions or calculation details may differ from the reference implementation and require further clarification.

## Reason-Code Generation

The following four reason codes were implemented using the available definitions and calculations:

| Code | Description | Transactions Flagged |
|---|---|---:|
| R01 | NEW_DEVICE | 7,305 |
| R03 | ODD_HOUR | 15,438 |
| R04 | FAILED_ATTEMPTS | 9,877 |
| R06 | NEW_ACCOUNT | 1,109 |

The following reason codes remain pending because their required rule definitions or thresholds were not available:

- R02 – GEO_MISMATCH
- R05 – AMOUNT_SPIKE
- R07 – VELOCITY
- R08 – HIGH_RISK_MCC

No arbitrary thresholds were introduced.

## Output File

The final reason-code output is:

`sentinel_reason_codes_output.csv`

- Total transactions: 110,000
- Output columns: `transaction_id`, `reason_codes`
- A transaction can contain multiple reason codes.
- Transactions without an assigned reason code are marked `NO_REASON_CODE`.

## Important Implementation Notes

- Historical feature calculations use only preceding transaction data.
- Night-time transactions are identified using Indian Standard Time (IST), from 00:00 to before 05:00.
- Distance is calculated using the Haversine formula.
- Missing or unavailable rule definitions are documented rather than replaced with guessed values.

## Project Status

- [x] Data quality analysis
- [x] Six features recomputed
- [x] Feature comparison completed
### Conclusion

The SENTINEL feature pipeline successfully recomputes six transaction features, validates them against the client-provided feature table, and generates reason-code output for 110,000 transactions.

Four reason codes are currently implemented. The remaining four require clarification of their rule definitions or thresholds before implementation.