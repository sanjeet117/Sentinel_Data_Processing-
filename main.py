
from src.data_loader import load_all_tables


def main():
    print("SENTINEL DATA PROCESSING PIPELINE")

    datasets = load_all_tables()

    print("\nData loading completed.")
    print("Loaded datasets:", list(datasets.keys()))


if __name__ == "__main__":
    main()
