from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
import warnings

# import visualization cards
from .visualizations.commits_over_time import gc_commits_over_time
from .visualizations.contribs_by_action import gc_contribs_by_action
from .visualizations.gh_company_affiliation import gc_gh_company_affiliation
from .visualizations.issues_closed import gc_issues_closed
from .visualizations.change_request_reviews import gc_change_request_reviews

warnings.filterwarnings("ignore")

dash.register_page(__name__, path="/community_activity")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(gc_commits_over_time, width=6),
                dbc.Col(gc_contribs_by_action, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
        dbc.Row(
            [
                dbc.Col(gc_gh_company_affiliation, width=6),
                dbc.Col(gc_issues_closed, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
        dbc.Row(
            [
                dbc.Col(gc_change_request_reviews, width=6),
            ],
            align="center",
            style={"marginBottom": ".5%"},
        ),
    ],
    fluid=True,
)
