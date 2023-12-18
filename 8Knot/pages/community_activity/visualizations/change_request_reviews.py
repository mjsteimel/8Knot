from dash import html, dcc, callback
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import logging
from dateutil.relativedelta import *  # type: ignore
import plotly.express as px
from pages.utils.graph_utils import get_graph_time_values, color_seq
from queries.contributors_query import contributors_query as ctq
import io
from cache_manager.cache_manager import CacheManager as cm
from pages.utils.job_utils import nodata_graph
import time


PAGE = "community_activity"
VIZ_ID = "change_request_reviews"

gc_change_request_reviews = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    "Change Request Reviews Over Time",
                    className="card-title",
                    style={"textAlign": "center"},
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph Info:"),
                        dbc.PopoverBody(
                            """
                            Visualizes the number of Change Request Reviews.
                            """
                        ),
                    ],
                    id=f"popover-{PAGE}-{VIZ_ID}",
                    target=f"popover-target-{PAGE}-{VIZ_ID}",  # needs to be the same as dbc.Button id
                    placement="top",
                    is_open=False,
                ),
                dcc.Loading(
                    dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
                ),
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Label(
                                    "Date Interval:",
                                    html_for=f"date-interval-{PAGE}-{VIZ_ID}",
                                    width="auto",
                                ),
                                dbc.Col(
                                    dbc.RadioItems(
                                        id=f"date-interval-{PAGE}-{VIZ_ID}",
                                        options=[
                                            {"label": "Month", "value": "M1"},
                                            {"label": "Quarter", "value": "M3"},
                                            {"label": "6 Months", "value": "M6"},
                                            {"label": "Year", "value": "M12"},
                                        ],
                                        value="M1",
                                        inline=True,
                                    ),
                                    className="me-2",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "About Graph",
                                        id=f"popover-target-{PAGE}-{VIZ_ID}",
                                        color="secondary",
                                        size="sm",
                                    ),
                                    width="auto",
                                    style={"paddingTop": ".5em"},
                                ),
                            ],
                            align="center",
                        ),
                    ]
                ),
            ]
        ),
    ],
)


# callback for graph info popover
@callback(
    Output(f"popover-{PAGE}-{VIZ_ID}", "is_open"),
    [Input(f"popover-target-{PAGE}-{VIZ_ID}", "n_clicks")],
    [State(f"popover-{PAGE}-{VIZ_ID}", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


# callback for commits over time graph
@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    [
        Input("repo-choices", "data"),
        Input(f"date-interval-{PAGE}-{VIZ_ID}", "value"),
    ],
    background=True,
)
def commits_over_time_graph(repolist, interval):
    # wait for data to asynchronously download and become available.
    cache = cm()
    df = cache.grabm(func=ctq, repos=repolist)
    while df is None:
        time.sleep(1.0)
        df = cache.grabm(func=ctq, repos=repolist)

    # data ready.
    start = time.perf_counter()
    logging.warning("COMMITS_OVER_TIME_VIZ - START")

    # test if there is data
    if df.empty:
        logging.warning("COMMITS OVER TIME - NO DATA AVAILABLE")
        return nodata_graph

    # function for all data pre processing
    df_created = process_data(df, interval)

    fig = create_figure(df_created, interval)

    logging.warning(f"COMMITS_OVER_TIME_VIZ - END - {time.perf_counter() - start}")
    return fig


def process_data(df: pd.DataFrame, interval):
    # convert to datetime objects rather than strings
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)

    # order values chronologically by COLUMN_TO_SORT_BY date
    df = df.sort_values(by="created_at", axis=0, ascending=True)

    # drop all contributions that are not the selected action
    df = df[df["Action"].str.contains("PR Review")]

    return df


def create_figure(df: pd.DataFrame, interval):
    # time values for graph
    x_r, x_name, hover, period = get_graph_time_values(interval)

    # create plotly express histogram
    fig = px.histogram(df, x="created_at", color_discrete_sequence=[color_seq[3]])

    # creates bins with interval size and customizes the hover value for the bars
    fig.update_traces(
        xbins_size=interval,
        hovertemplate=hover + "<br>" + "PR Reviews: %{y}<br><extra></extra>",
        marker_line_width=0.1,
        marker_line_color="black",
    )

    # update xaxes to align for the interval bin size
    fig.update_xaxes(
        showgrid=True,
        ticklabelmode="period",
        dtick=period,
        rangeslider_yaxis_rangemode="match",
        range=x_r,
    )

    # layout styling
    fig.update_layout(
        xaxis_title=x_name,
        yaxis_title="PR Reviews",
        margin_b=40,
        font=dict(size=14),
    )

    return fig
