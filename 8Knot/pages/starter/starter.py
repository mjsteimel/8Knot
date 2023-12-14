from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
import warnings

# import visualization cards
from .visualizations.time_first_response import gc_time_first_response
from .visualizations.issues_closed import gc_issues_closed

warnings.filterwarnings("ignore")

dash.register_page(__name__, path="/starter")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(gc_time_first_response, width=6),
                dbc.Col(gc_issues_closed, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
    ],
    fluid=True,
)
