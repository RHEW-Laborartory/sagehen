import pandas as pd
import sqlite3

from SagePy.iplotBuilder import iplot_labeler


DATABASE = sqlite3.connect("sagehen.db")

column_dict = {
    'date_time':
        {
         'label': 'Year',
         'color': 'green',
        },
    'solar_rad':
        {
         'label': 'K W-hr/m^2',
         'color': 'red',
        },
    'wind_ave':
        {
         'label': 'Velocity (m/s)',
         'color': 'cornflowerblue',
        },
    'wind_dir':
        {
         'label': 'Degrees',
         'color': 'crimson',
        },
    'wind_max':
        {
         'label': 'Velocity (m/s)',
         'color': 'tomato',
        },
    'temp_ave':
        {
         'label': 'Temperature (ºC)',
         'color': 'gold',
        },
    'temp_max':
        {
         'label': 'Temperature (ºC)',
         'color': 'orangered',
        },
    'temp_min':
        {
         'label': 'Temperature (ºC)',
         'color': 'dodgerblue',
        },
    'soil_tave':
        {
         'label': 'Temperature (ºC)',
         'color': 'lightseagreen',
        },
    'soil_tmax':
        {
         'label': 'Temperature (ºC)',
         'color': 'darkcyan',
        },
    'soil_tmin':
        {
         'label': 'Temperature (ºC)',
         'color': 'paleturquoise',
        },
    'rh_ave':
        {
         'label': 'RH (%)',
         'color': 'slateblue',
        },
    'rh_max':
        {
         'label': 'RH (%)',
         'color': 'indigo',
        },
    'rh_min':
        {
         'label': 'RH (%)',
         'color': 'plum',
        },
    'dew_pt':
        {
         'label': 'Temperature (ºC)',
         'color': 'orange',
        },
    'wet_bulb':
        {
         'label': 'Temperature (ºC)',
         'color': 'darkcyan',
        },
    'pressure':
        {
         'label': 'Temperature (ºC)',
         'color': 'blueviolet',
        },
    'snow':
        {
         'label': 'Millimeters',
         'color': 'deepskyblue',
        },
    'precip':
        {
         'label': 'Millimeters',
         'color': 'royalblue',
        },
}


def col_colors(pandas_obj):
    try:
        if type(pandas_obj) == pd.core.frame.DataFrame:
            colors = [column_dict[col]['color'] for col in pandas_obj.columns]
        elif type(pandas_obj) == pd.core.series.Series:
            colors = [column_dict[pandas_obj.name]['color']]
        return colors
    except KeyError:
        return None


def _plot_labels(pandas_obj, x_label, y_label):
    if x_label is None:
        try:
            x_label = column_dict[pandas_obj.index.name]["label"]
        except KeyError as missing_key:
            x_label = str(missing_key).replace("'", "").title()
    if y_label is None:
        try:
            if type(pandas_obj) == pd.core.series.Series:
                y_label = column_dict[pandas_obj.name]['label']
            elif type(pandas_obj) == pd.core.frame.DataFrame:
                y_label = column_dict[pandas_obj.columns[0]]['label']
        except KeyError as missing_key:
            pass
    return x_label, y_label


def sage_iplot(pandas_obj, title=None, x_label=None, y_label=None, **kwds):
    x, y = _plot_labels(pandas_obj, x_label, y_label)
    layout = iplot_labeler(title, x, y)
    color = col_colors(pandas_obj)
    return pandas_obj.iplot(
        color=color,
        layout=layout,
        **kwds,
    )


def sage_plot(
        pandas_obj, figsize=(16, 8), 
        x_label=None, y_label=None, **kwds):
    x, y = _plot_labels(pandas_obj, x_label, y_label)
    color = col_colors(pandas_obj)
    if color is None or 'colormap' in kwds.keys():
        ax = pandas_obj.plot(
            figsize=figsize,
            **kwds,
        )
    elif 'colormap' not in kwds.keys():
        ax = pandas_obj.plot(
            color=color,
            figsize=figsize,
            **kwds,
        )
    try:
        ax.set_xlabel(x)
        ax.set_ylabel(y)
    except AttributeError:
        pass
    return ax


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
    results = pd.read_sql(
        sql_query,
        con=DATABASE
    )
    return _config_df(results)
