from pathlib import Path
from _csv import reader
from statistics import mean, median


class CSVFile:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)
        self.rows: list[tuple[str, ...]] = []
        self.read()

    def read(self) -> None:
        with self.filename.open("r", encoding="utf-8", newline="") as file:
            self.rows = [tuple(row) for row in reader(file)]

    def get_rows(self) -> list[tuple[str, ...]]:
        return self.rows

    def get_rows_as_lists(self) -> list[list[str]]:
        return [list(row) for row in self.rows]

    def get_column_names(self) -> list[str]:
        if not self.rows:
            return []

        return list(self.rows[0])

    def get_column_index(self, column_name: str) -> int:
        return self.get_column_names().index(column_name)

    def count_values(self, column_name: str) -> dict[str, int]:
        column_index = self.get_column_index(column_name)
        counts: dict[str, int] = {}

        for row in self.rows[1:]:
            value = row[column_index]
            counts[value] = counts.get(value, 0) + 1

        return counts

    def percentage_values(self, column_name: str) -> dict[str, float]:
        counts = self.count_values(column_name)
        total = sum(counts.values())

        if total == 0:
            return {}

        return {
            value: count / total * 100
            for value, count in counts.items()
        }

    def average_and_median_by_group(
        self, group_column: str, value_columns: list[str]
    ) -> dict[str, dict[str, dict[str, float]]]:
        group_index = self.get_column_index(group_column)
        value_indexes = {
            column_name: self.get_column_index(column_name)
            for column_name in value_columns
        }
        grouped_values: dict[str, dict[str, list[float]]] = {}

        for row in self.rows[1:]:
            group_name = row[group_index]
            grouped_values.setdefault(
                group_name,
                {column_name: [] for column_name in value_columns}
            )

            for column_name, column_index in value_indexes.items():
                grouped_values[group_name][column_name].append(
                    float(row[column_index])
                )

        return {
            group_name: {
                column_name: {
                    "average": mean(values),
                    "median": median(values),
                }
                for column_name, values in columns.items()
            }
            for group_name, columns in grouped_values.items()
        }
