
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


PRIMARY_KEYS = {
    "customers": "customer_id",
    "merchants": "merchant_id",
    "devices": "device_id",
    "transactions": "transaction_id",
    "payment_outcomes": "transaction_id",
    "labels": "transaction_id",
    "features": "transaction_id",
}


def generate_null_report(datasets):
    """Count missing values in every column of every dataset."""

    records = []

    for table_name, df in datasets.items():
        for column in df.columns:
            records.append({
                "table": table_name,
                "column": column,
                "null_count": int(df[column].isna().sum()),
                "null_percentage": round(
                    df[column].isna().mean() * 100, 2
                )
            })

    report = pd.DataFrame(records)
    report.to_csv(REPORT_DIR / "null_report.csv", index=False)

    return report


def generate_duplicate_report(datasets):
    """Report exact duplicate rows and duplicate primary keys."""

    records = []

    for table_name, df in datasets.items():
        exact_duplicates = int(df.duplicated().sum())

        primary_key = PRIMARY_KEYS.get(table_name)

        duplicate_keys = 0
        if primary_key and primary_key in df.columns:
            duplicate_keys = int(
                df[primary_key].duplicated().sum()
            )

        records.append({
            "table": table_name,
            "row_count": len(df),
            "exact_duplicate_rows": exact_duplicates,
            "duplicate_primary_keys": duplicate_keys
        })

    report = pd.DataFrame(records)
    report.to_csv(REPORT_DIR / "duplicate_report.csv", index=False)

    return report


def generate_type_report(datasets):
    """Report column data types and invalid values in key fields."""

    records = []

    numeric_columns = [
        "transaction_amount",
        "amount_paise",
        "customer_age",
        "account_age",
        "previous_transactions",
        "average_transaction_value",
        "failed_transactions"
    ]

    timestamp_columns = [
        "transaction_time",
        "outcome_time",
        "label_available_at"
    ]

    for table_name, df in datasets.items():
        for column in df.columns:
            invalid_count = 0

            if column in numeric_columns:
                converted = pd.to_numeric(
                    df[column], errors="coerce"
                )
                invalid_count = int(
                    (df[column].notna() & converted.isna()).sum()
                )

            elif column in timestamp_columns:
                converted = pd.to_datetime(
                    df[column], errors="coerce", utc=True
                )
                invalid_count = int(
                    (df[column].notna() & converted.isna()).sum()
                )

            records.append({
                "table": table_name,
                "column": column,
                "detected_dtype": str(df[column].dtype),
                "invalid_value_count": invalid_count
            })

    report = pd.DataFrame(records)
    report.to_csv(REPORT_DIR / "data_type_report.csv", index=False)

    return report


def generate_amount_outlier_report(datasets):
    """Identify transaction amount outliers using the IQR method."""

    transactions = datasets["transactions"].copy()

    amount_column = (
        "transaction_amount"
        if "transaction_amount" in transactions.columns
        else "amount_paise"
    )

    amounts = pd.to_numeric(
        transactions[amount_column], errors="coerce"
    )

    valid_amounts = amounts.dropna()

    if valid_amounts.empty:
        report = pd.DataFrame(columns=[
            "transaction_id",
            "amount",
            "lower_bound",
            "upper_bound"
        ])
    else:
        q1 = valid_amounts.quantile(0.25)
        q3 = valid_amounts.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        mask = (
            (amounts < lower_bound) |
            (amounts > upper_bound)
        )

        report = pd.DataFrame({
            "transaction_id": transactions.loc[
                mask, "transaction_id"
            ],
            "amount": amounts[mask],
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        })

    report.to_csv(
        REPORT_DIR / "amount_outliers.csv",
        index=False
    )

    return report


def generate_split_report(datasets):
    """Count transactions in each dataset split."""

    transactions = datasets["transactions"]

    if "split" not in transactions.columns:
        report = pd.DataFrame(columns=["split", "row_count"])
    else:
        report = (
            transactions["split"]
            .value_counts(dropna=False)
            .rename_axis("split")
            .reset_index(name="row_count")
        )

    report.to_csv(REPORT_DIR / "split_report.csv", index=False)

    return report


def generate_data_quality_report(datasets):
    """Generate all data quality reports."""

    print("Generating data quality reports...")

    reports = {
        "nulls": generate_null_report(datasets),
        "duplicates": generate_duplicate_report(datasets),
        "data_types": generate_type_report(datasets),
        "amount_outliers": generate_amount_outlier_report(datasets),
        "splits": generate_split_report(datasets)
    }

    print("Data quality reports generated.")

    return reports
