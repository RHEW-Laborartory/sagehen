
def iplot_labeler(g_title, x_axis, y_axis):
    """
    Creates a dictionary object structured for Plotly's
    iplot layout parameter

    Parameters
    ----------
    g_title : string (optional)
        provide a title for your plot
    x_axis : string (optional)
        provide a title for your x-axis
    y_axis : string (optional)
        provide a title for your y-axis

    Returns
    -------
    python.dict()
        Dictionary formatted for plotly.iplot's layout argument
    """
    return dict(
        title=g_title,
        xaxis=dict(title=x_axis),
        yaxis=dict(title=y_axis),
        )
