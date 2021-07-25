import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sim import simirality_df, Similarity

lat_lon_df = pd.read_csv('./lat_lon_df.csv', sep=';')
sim = Similarity(simirality_df, 'ehddnr', '콘텐츠디자인@UI/UX디자인@웹디자인@Sketch@figma', 'cosine')

idxs = sim.get_item()

# if idxs:
df = pd.DataFrame(idxs, columns=['recruit_id'])

my_recruit_df = pd.merge(left=df, right=lat_lon_df, how='left', on='recruit_id')
my_recruit_df['info_address'].fillna('재택', inplace=True)
my_recruit_df.fillna(0, inplace=True)
my_recruit_df['lat'] = my_recruit_df['lat'].apply(lambda x : round(x,4))
my_recruit_df['lon'] = my_recruit_df['lon'].apply(lambda x : round(x,4))

map_df = my_recruit_df[my_recruit_df['lat'] != 0]

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

fig = px.scatter_mapbox(map_df,
                        lat='lat',
                        lon='lon',
                        color='recruit_id',
                        hover_data=['info_address'],
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=10,
                      )

fig.update_layout(mapbox_style='carto-positron')
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})


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
            style={"textAlign": "center", "paddingTop": "50px", 'marginBottom': '50px'},
            children=[html.H1("Locket Punch", style={"fontSize": 50})],
        ),
        html.Div(
            style={'display':'flex', 'alginItems':'center', 'justifyContent': 'center'},
            children=[
                html.Div(
                    style={"marginRight": "30px"},
                    children=[
                        dcc.Graph(figure=fig)
                    ]
                ),
                html.Table(
                    style={'textAlign':'center'},
                    children=[
                    html.Thead(
                        children=[
                            html.Tr(
                                children=[
                                    html.Th(col) for col in my_recruit_df.columns
                                ]
                            )
                        ]
                    ),
                    html.Tbody(
                        children=[
                            html.Tr(
                                children=[
                                    html.Td(
                                        style={'padding':'10px'},
                                        children=[val]
                                    )  for val in values
                                ] 
                            ) 
                            for values in my_recruit_df.values
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