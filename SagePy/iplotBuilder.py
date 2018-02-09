
def iplot_labeler(title=None, x=None, y=None):
    """
    Creates a dictionary object structured for Plotly's
    iplot layout parameter

    Parameters
    ----------
    title : string (optional)
        provide a title for your plot
    x : string (optional)
        provide a title for your x-axis
    y : string (optional)
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
