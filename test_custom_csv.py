from custom_csv import CustomCsvReader, CustomCsvWriter
import csv

def main() -> None:
    rows = [
        ["id", "name", "note"],
        ["1", 'Alice "A"', "hello,world"],
        ["2", "Bob", "multi\nline text"],
        ["3", "comma,inside", 'quote "inside" and,comma'],
        ["4", "", ""],
    ]

    with open("test_custom.csv", "w", encoding="utf-8", newline="") as f:
        writer = CustomCsvWriter(f)
        writer.writerows(rows)
    with open("test_custom.csv", "r", encoding="utf-8", newline="") as f:
        std_rows = list(csv.reader(f))
    with open("test_custom.csv", "r", encoding="utf-8", newline="") as f:
        custom_rows = list(CustomCsvReader(f))

    print("Standard:", std_rows)
    print("Custom:  ", custom_rows)
    print("Match?  ", std_rows == custom_rows)


if __name__ == "__main__":
    main()
    