import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sim import simirality_df, Similarity

sim = Similarity(simirality_df, 'ehddnr', 'python@javascript@AWS@Django@브랜드마케팅', 'cosine')

idxs = sim.get_item()

# if idxs:
df = pd.DataFrame(idxs, columns=['recruit_id'])


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]


app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",        
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Locket Punch", style={"fontSize": 50})],
        ),
        html.Div(
            children=[
                html.Table(
                    children=[
                    html.Thead(
                        children=[
                            html.Tr(
                                children=[
                                    html.Th(col) for col in df.columns
                                ]
                            )
                        ]
                    ),
                    html.Tbody(
                        children=[
                            html.Tr(
                                children=[
                                    html.Td(val)  for val in values
                                ] 
                            ) 
                            for values in df.values
                        ]
                    )
                  ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)