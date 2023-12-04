from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
import warnings

# import visualization cards
from .visualizations.bus_factor import gc_bus_factor
from .visualizations.time_first_response import gc_time_first_response
from .visualizations.placeholder3 import gc_placeholder3
from .visualizations.release_frequency import gc_release_frequency

warnings.filterwarnings("ignore")

dash.register_page(__name__, path="/starter_health")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(gc_bus_factor, width=6),
                dbc.Col(gc_time_first_response, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
        dbc.Row(
            [
                dbc.Col(gc_release_frequency, width=6),
                dbc.Col(gc_placeholder3, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
    ],
    fluid=True,
)
