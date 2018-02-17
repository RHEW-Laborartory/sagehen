import csv
import datetime


filepath = input("Enter CSV filepath: ")
start_date = input("Start Date (YYYY-MM-DD): ")

missing_dates = []


def _add_one_day(date):
    """Increases the date by one day using the datetime library"""
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    return date


def main():
    with open(filepath) as CSVfile:
        readCSV = csv.DictReader(CSVfile, delimiter=",")
        current_date = start_date
        for row in readCSV:
            # print(row['date'], current_date)
            # input()
            if row['date'] != current_date:
                missing_dates.append(row['date'])
            current_date = _add_one_day(current_date)

    print(missing_dates)


if __name__ == "__main__":
    main()