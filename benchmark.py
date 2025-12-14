import csv
import os
import timeit
from typing import List

from custom_csv import CustomCsvReader, CustomCsvWriter


def generate_dataset(n_rows: int = 10000, n_cols: int = 5) -> List[List[str]]:
    """
    Generate a synthetic dataset with commas, quotes, and newlines
    to stress-test the CSV reader and writer.
    """
    rows: List[List[str]] = []

    for i in range(n_rows):
        row: List[str] = []
        for j in range(n_cols):
            base = f"row{i}_col{j}"
            if j == 1:
                value = base + ",with,commas"
            elif j == 2:
                value = base + ' "with quotes"'
            elif j == 3:
                value = base + "\nwith newline"
            else:
                value = base
            row.append(value)
        rows.append(row)

    return rows


def write_with_std(path: str, rows: List[List[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def write_with_custom(path: str, rows: List[List[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = CustomCsvWriter(file)
        writer.writerows(rows)


def read_with_std(path: str) -> None:
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for _ in reader:
            pass


def read_with_custom(path: str) -> None:
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = CustomCsvReader(file)
        for _ in reader:
            pass


def main() -> None:
    dataset = generate_dataset()
    temp_std = "benchmark_std.csv"
    temp_custom = "benchmark_custom.csv"
    runs = 3
    std_write = timeit.timeit(
        lambda: write_with_std(temp_std, dataset),
        number=runs,
    ) / runs

    custom_write = timeit.timeit(
        lambda: write_with_custom(temp_custom, dataset),
        number=runs,
    ) / runs
 
    std_read = timeit.timeit(
        lambda: read_with_std(temp_std),
        number=runs,
    ) / runs

    custom_read = timeit.timeit(
        lambda: read_with_custom(temp_custom),
        number=runs,
    ) / runs


    if os.path.exists(temp_std):
        os.remove(temp_std)
    if os.path.exists(temp_custom):
        os.remove(temp_custom)

    print("=== Benchmark Results (average over", runs, "runs) ===")
    print(f"csv.writer write time       : {std_write:.6f} seconds")
    print(f"CustomCsvWriter write time  : {custom_write:.6f} seconds")
    print()
    print(f"csv.reader read time        : {std_read:.6f} seconds")
    print(f"CustomCsvReader read time   : {custom_read:.6f} seconds")


if __name__ == "__main__":
    main()
