from typing import List
import pandas as pd


def main():
    # continually ask for a valid filename until one is received
    while True:
        filename = input("Enter a file name: ")
        if is_valid_filename(filename):
            break

    # main program loop
    while True:
        column_num = select_column_number()

        # number of records to retrieve (maximum 100)
        n_records = 6

        if not 1 < n_records < 100:
            print('Number of records shown must be from 1 to 100: showing 6 instead...\n')

        # print statements for low values
        print(f"\nLowest values for column {column_num}:")

        low_values = lowest_values(averages(filename, column_num), n_records)
        for value in low_values:
            print("Date: {}, Value: {val: > 6.2f}".format(value[0], val=value[1]))
        print()

        # print statements for high values
        print(f"Highest values for column {column_num}:")

        high_values = highest_values(averages(filename, column_num), n_records)
        for value in high_values:
            print("Date: {}, Value: {value: > 6.2f}".format(value[0], value=value[1]))
        print()

        # Ask to continue, and validate the user input
        while True:
            try:
                choice = input("\nDo you want to continue? Y or N: ").upper().strip()[0]
                if choice == 'Y':
                    break
                elif choice == 'N':
                    print('\nBye!')
                    exit(0)
                else:
                    print('Invalid entry')

            except IndexError:
                print("Please type Yes or No")


def is_valid_filename(filename: str) -> bool:
    try:
        with open(filename):
            return True
    except FileNotFoundError:
        print('Bad filename.')
    return False


def file_generator(filename: str):
    for row in open(filename):
        yield row.strip().split(sep=',')


def select_column_number() -> int:
    while True:
        try:
            column_number = int(input("Enter a column number 1 to 6: "))
            if not 0 < column_number < 7:
                print("Invalid column, try again.")
            else:
                return column_number
        except ValueError:
            print("Error: please enter an integer.")


def lowest_values(series: pd.Series, n_records: int = 6) -> List[tuple]:
    if not 1 < n_records < 100:
        n_records = 6
    series_n_rows = series.sort_values(ascending=True).head(n_records)
    return list(zip(series_n_rows.index.strftime('%Y-%m'), series_n_rows))


def highest_values(series: pd.Series, n_records: int = 6) -> List[tuple]:
    if not 1 < n_records < 100:
        n_records = 6
    series_n_rows = series.sort_values(ascending=False).head(n_records)
    return list(zip(series_n_rows.index.strftime('%Y-%m'), series_n_rows))


def averages(filename: str, column_n: int) -> pd.Series:
    generator = file_generator(filename)
    columns = list(next(generator))  # set column names

    df = pd.DataFrame(generator, columns=columns)

    # convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # convert the rest of the columns to float64
    df[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']] = \
        df[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']].apply(pd.to_numeric)

    series = df.groupby(pd.PeriodIndex(df['Date'], freq="M"))[columns[column_n]]
    return series.mean()


if __name__ == '__main__':
    main()
