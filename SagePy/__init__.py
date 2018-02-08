import pandas as pd
import sqlite3


DATABASE = sqlite3.connect("sagehen.db")

plt_colors = {
    'solar_rad': 'red',
    'wind_ave': 'cornflowerblue',
    'wind_dir': 'crimson',
    'wind_max': 'tomato',
    'temp_ave': 'gold',
    'temp_max': 'orangered',
    'temp_min': 'dodgerblue',
    'soil_tave': 'lightseagreen',
    'soil_tmax': 'darkcyan',
    'soil_tmin': 'paleturquoise',
    'rh_ave': 'slateblue',
    'rh_max': 'indigo',
    'rh_min': 'plum',
    'dew_pt': 'orange',
    'wet_bulb': 'darkcyan',
    'pressure': 'blueviolet',
    'snow': 'deepskyblue',
    'precip': 'royalblue',
}


def col_colors(pandas_obj):
    if type(pandas_obj) == pd.core.frame.DataFrame:
        colors = [plt_colors[col] for col in pandas_obj.columns]
    elif type(pandas_obj) == pd.core.series.Series:
        colors = [plt_colors[pandas_obj.name]]
    return colors


def _config_df(pandas_obj):
    """
    Configures a Pandas DataFrame or Series to a set of specifications

    Parameters
    ----------
    pandas_obj : pandas.DataFrame or pandas.Series
        Pandas Dataframe that will be configured with the following
        specifications:
        - Remove sql id
        - Change values in date_time column to actual python.datetime
            objects.
        - Sets date_time column to Index Column in pandas.DataFrame or
            pandas.Series
        - Assures all values in pandas.DataFrame are numeric, and not
            type string

    Returns
    -------
    pandas_obj : pandas.DataFrame or pandas.Series
    """
    pandas_obj.drop('id', axis=1, inplace=True)
    pandas_obj['date_time'] = pd.to_datetime(
        pandas_obj['date_time'],
        errors="coerce",
    )
    pandas_obj.set_index(['date_time'], inplace=True)
    pandas_obj = pandas_obj.apply(pd.to_numeric, args=('coerce',))
    return pandas_obj


def _column_adder(cols_wanted):
    """Adds the list of columns
    into a string object, seperated by commas

    Parameters
    ----------
    cols_wanted : list
        List of column strings to be added to sql query

    Returns
    -------
    select_cols : string
        A string of each column name seperated by a comma
    """
    if not cols_wanted:
        select_cols = "*"
    else:
        select_cols = 'id,date_time'
        for column in cols_wanted:
            select_cols += "," + column
    return select_cols


def year_search(start_yr, end_yr, cols_wanted=[]):
    """Returns a Pandas DataFrame or Series with rows matching the specified
    year range
    """
    select_cols = _column_adder(cols_wanted)
    sql_query = "SELECT {0} FROM hourdata WHERE date_time >= '{1}-01-01' AND date_time <= '{2}-12-31';".format(select_cols, start_yr, end_yr)
    results = pd.read_sql(
        sql_query,
        con=DATABASE,
    )
    return _config_df(results)


def date_search(start_date, end_date, cols_wanted=[]):
    """Returns a Pandas DataFrame or Series with rows matching the specified date
    range
    """
    select_cols = _column_adder(cols_wanted)
    sql_query = "SELECT {0} FROM hourdata WHERE date_time >= '{1}' AND date_time <= '{2}';".format(select_cols, start_date, end_date)
    results = pd.read_sql(
        sql_query,
        con=DATABASE,
    )
    return _config_df(results)


def value_search(col, start_val, end_val, cols_wanted=[]):
    """
    Returns a Pandas DataFrame or Series with the rows matching the specified
    value range within the specified column
    """
    if cols_wanted:
        cols_wanted.append(col)
    select_cols = _column_adder(cols_wanted)

    sql_query = "SELECT {3} FROM hourdata WHERE {0} >= {1} AND {0} <= {2} AND {0} IS NOT NULL;".format(col, start_val, end_val, select_cols)
    print(sql_query)
    results = pd.read_sql(
        sql_query,
        con=DATABASE
    )
    return _config_df(results)
