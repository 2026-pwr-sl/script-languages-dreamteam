import sys
from pathlib import Path

from csv_file import CSVFile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def get_dataset_path(dataset_name: str) -> Path:
    if not dataset_name.endswith(".csv"):
        raise ValueError("Dataset file must have a .csv extension.")

    dataset_path = DATA_DIR / dataset_name

    if not dataset_path.is_file():
        raise FileNotFoundError(
            f"Dataset file '{dataset_name}' does not exist in data/."
        )

    return dataset_path


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python app8.py dataset.csv")
        raise SystemExit(1)

    dataset_name = sys.argv[1]

    try:
        dataset_path = get_dataset_path(dataset_name)
    except ValueError as error:
        print(f"Error: {error}")
        raise SystemExit(1)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    print(f"Dataset file found: {dataset_path}")

    data = CSVFile(dataset_path)
    print(f"Column names: {data.get_column_names()}")

    paid_subscription_counts = data.count_values("Paid_Subscription")
    paid_subscription_percentages = data.percentage_values("Paid_Subscription")

    print("\nPaid subscription counts:")
    print(
        "Students with paid subscription: "
        f"{paid_subscription_counts.get('True', 0)} "
        f"({paid_subscription_percentages.get('True', 0):.2f}%)"
    )
    print(
        "Students without paid subscription: "
        f"{paid_subscription_counts.get('False', 0)} "
        f"({paid_subscription_percentages.get('False', 0):.2f}%)"
    )

    stats = data.average_and_median_by_group(
        "Paid_Subscription",
        ["Pre_Semester_GPA", "Post_Semester_GPA"],
    )

    print("\nAverage and median GPA grouped by Paid_Subscription:")
    for group_name, columns in stats.items():
        print(f"\nPaid_Subscription = {group_name}")
        for column_name, values in columns.items():
            average = values["average"]
            median = values["median"]
            print(
                f"{column_name}: average = {average:.3f}, "
                f"median = {median:.3f}"
            )


if __name__ == "__main__":
    main()
