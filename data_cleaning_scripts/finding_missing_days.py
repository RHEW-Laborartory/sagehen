import csv


missing_days = []

with open('/Users/lawerencelee/rhew_lab/WU_Scraper/KTRK_1948-01-01_2017-02-13.csv') as CSVfile:
    readCSV = csv.reader(CSVfile, delimiter=",")
    set_day = 1
    set_month = 1
    set_year = 1948
    for row in readCSV:
        if row[0] != 'date':
            year, month, day = row[0].split('-')
            year = int(year)
            month = int(month)
            day = int(day)

            if set_day != day or set_month != month or set_year != year:
                if set_year+1 == year:
                    set_year += 1
                    set_month = 1
                    set_day = 1
                elif set_month+1 == month:
                    set_month += 1
                    set_day = 1
                else:
                    if set_day+1 != day:
                        # print(year, month, "day Change: {} --> {}".format(set_day, day))
                        missing_days.append([year, month, set_day+1, day]) 
                        set_day = day
                    else:
                        set_day += 1


print(missing_days)