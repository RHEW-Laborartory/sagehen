#!/usr/bin/python
''' Systematically checks each day of the specified period for
changes in the data columns. '''

import os

from selenium.common.exceptions import (NoSuchElementException)
from selenium import webdriver
from selenium.webdriver.support.ui import Select

BROWSER = webdriver.Firefox()
ALL_DATA_cols = []
DATES_WITHOUT_DATA = []
CURRENT_COL_ARRANGEMENT = ''

# User Variables
beginning_year = 1997
end_year = 2017


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_date(year_num, month_num, day_num):
    BROWSER.get("https://wrcc.dri.edu/cgi-bin/wea_daysum.pl?casagh")

    year_element = BROWSER.find_element_by_xpath(
                                                '/html/body/form/select[3]')
    year_select = Select(year_element)
    year_select.select_by_visible_text(str(year_num))

    month_element = BROWSER.find_element_by_xpath(
                                                "/html/body/form/select[1]")
    month_select = Select(month_element)
    month_select.select_by_index(month_num-1)

    day_element = BROWSER.find_element_by_xpath(
                                            "/html/body/form/select[2]")
    day_select = Select(day_element)
    day_select.select_by_index(day_num-1)

    submit_button = BROWSER.find_element_by_xpath(
                                        "/html/body/form/input[3]")
    submit_button.click()

    return year_num, month_num, day_num


def grab_data(date):

    year, month, day = date
    try:
        center_element = BROWSER.find_element_by_xpath(
                                            "/html/body/center")
    except NoSuchElementException:
        bad_date = "{}-{}-{}".format(year, month, day)
        DATES_WITHOUT_DATA.append(bad_date)
        print('NO DATA ON: {}'.format(bad_date))
        return False

    if "data not available" in center_element.text.lower():
        bad_date = "{}-{}-{}".format(year, month, day)
        DATES_WITHOUT_DATA.append(bad_date)
        print('NO DATA ON: {}'.format(bad_date))
        return False

    data_cols = ''
    for num in range(1, 5):
        element = BROWSER.find_element_by_xpath('/html/body/center[3]/table/tbody/tr[{}]'.format(num))
        data_cols += element.text

    if data_cols not in ALL_DATA_cols:
        ALL_DATA_cols.append(data_cols)
        print("New column arrangement on {}-{}-{}".format(year, month, day))

    global CURRENT_COL_ARRANGEMENT
    if data_cols != CURRENT_COL_ARRANGEMENT:
        print(data_cols)
        CURRENT_COL_ARRANGEMENT = data_cols


if __name__ == "__main__":
    clear()
    print('<<<<<<< Sagehen Climate Data Web Scraper >>>>>>>')
    for year in range(beginning_year, end_year + 1):
        print('YEAR: ', year)
        for month in range(1, 13):
            print('MONTH: ', month)
            for day in range(1, 32):
                if year == 1997 and month in [1, 2, 3, 11]:
                    bad_date = "{}-{}-{}".format(year, month, day)
                    DATES_WITHOUT_DATA.append(bad_date)
                elif year == 2005 and month in [4, 5]:
                    bad_date = "{}-{}-{}".format(year, month, day)
                    DATES_WITHOUT_DATA.append(bad_date)
                else:
                    date = choose_date(year, month, day)
                    if date:
                        grab_data(date)
    os.system("say 'Sagehen Web Scraper Finished'")
