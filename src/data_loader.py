
import os
import pickle
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

TABLES = {
    "customers": "customer_id",
    "merchants": "merchant_id",
    "devices": "device_id",
    "transactions": "transaction_id",
    "payment_outcomes": "transaction_id",
    "labels": "transaction_id",
    "features": "transaction_id",
}

BATCH_SIZE = 1000


def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL or SUPABASE_KEY is missing in .env"
        )

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def load_table(client, table_name, primary_key):
    print(f"Loading table: {table_name}")

    all_rows = []
    start = 0

    while True:
        response = (
            client.table(table_name)
            .select("*")
            .order(primary_key)
            .range(start, start + BATCH_SIZE - 1)
            .execute()
        )

        rows = response.data or []

        if not rows:
            break

        all_rows.extend(rows)
        start += len(rows)

        if len(rows) < BATCH_SIZE:
            break

    dataframe = pd.DataFrame(all_rows)

    print(f"Loaded {len(dataframe):,} rows from {table_name}")

    return dataframe


def load_all_tables():
    client = get_supabase_client()

    datasets = {}

    for table_name, primary_key in TABLES.items():
        datasets[table_name] = load_table(
            client,
            table_name,
            primary_key
        )

    output_path = OUTPUT_DIR / "raw_data.pkl"

    with open(output_path, "wb") as file:
        pickle.dump(datasets, file)

    print(f"\nRaw datasets saved to: {output_path}")

    return datasets
