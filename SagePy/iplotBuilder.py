
def iplot_labeler(title=None, x=None, y=None):
    """
    Creates a dictionary object structured for Plotly's
    iplot layout parameters

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
        title=title,
        xaxis=dict(title=x),
        yaxis=dict(title=y),
        )
