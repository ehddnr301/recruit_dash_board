from fig import get_df_n_fig
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from w2v_sim import W2VSimilarity


speciality = ' '

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]
init = pd.DataFrame(columns=['recruit_id','info_address','lat','lon'])

my_recruit_df, fig = get_df_n_fig(speciality)


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
            children=[html.H1("Locket Punch 채용기반 직업추천", style={"fontSize": 35})],
        ),
        html.Div(
            style={'width':'100%', 'display':'flex', 'flexDirection':'column', 'alignItems':'center', 'marginBottom': '20px'},
            children=[
                html.Div(
                    style={'display':'flex', 'marginBottom':'10px', 'width':'50%'},
                    children=[
                        dcc.Input(
                            style={'width': '90%', 'padding':'10px', 'borderRadius':'10px', 'marginRight':'15px'},
                            id='ipt',
                            type='text',
                            placeholder='활동분야를 띄워쓰기로 구분해서 써주세요'
                        ),
                        html.Button(
                            id='btn',
                            children=['제출'],
                            style={'color':'black', 'backgroundColor':'white', 'fontSize':'14px', 'padding':'5px', 'borderRadius':'5px', 'width':'50px'}
                        )
                    ]
                ),
                html.Div(
                    id='my-div'
                )
            ]
        ),
        
        html.Div(
            style={'display':'flex', 'alginItems':'center', 'justifyContent': 'center'},
            children=[
                html.Div(
                    style={"marginRight": "30px"},
                    children=[
                        dcc.Graph(id='fig')
                    ]
                ),
                html.Div(
                    children=[
                        dash_table.DataTable(
                            style_cell={'textAlign':'center', 'backgroundColor':'black', 'color':'white', 'border':'1px solid white'},
                            id='table',
                            columns=[{'name': i, 'id':i} for i in init.columns],
                            # data= init.to_dict('records')
                        )
                    ]
                )
            ]
        ),


        html.Div(
            style={'width':'100%', 'display':'flex', 'flexDirection':'column', 'alignItems':'center', 'marginBottom': '20px', 'margin':'35px 0','borderTop':'1px dashed #ffa801', 'paddingTop':'20px'},
            children=[
                html.Div(
                    style={'display':'flex', 'marginBottom':'10px', 'width':'50%'},
                    children=[
                        dcc.Input(
                            style={'width': '90%', 'padding':'10px', 'borderRadius':'10px', 'marginRight':'15px'},
                            id='ipt2',
                            type='text',
                            placeholder='활동소개를 아무렇게나 써주세요.'
                        ),
                        html.Button(
                            id='btn2',
                            children=['제출'],
                            style={'color':'black', 'backgroundColor':'white', 'fontSize':'14px', 'padding':'5px', 'borderRadius':'5px', 'width':'50px'}
                        )
                    ]
                ),
                html.Div(
                    id='my-div2'
                )
            ]
        ),

        html.Div(
            style={'display':'flex', 'alginItems':'center', 'justifyContent': 'center', },
            children=[
                html.Div(
                    style={"marginRight": "30px"},
                    children=[
                        dcc.Graph(id='fig2')
                    ]
                ),
                html.Div(
                    children=[
                        dash_table.DataTable(
                            style_cell={'textAlign':'center', 'backgroundColor':'black', 'color':'white', 'border':'1px solid white'},
                            id='table2',
                            columns=[{'name': i, 'id': f'{i}_2'} for i in init.columns],
                            data= init.to_dict('records')
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [Output(component_id='my-div', component_property='children'),
    Output(component_id='fig', component_property='figure'),
    # Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data')],

    [Input('btn', 'n_clicks')],
    state=[State(component_id='ipt', component_property='value')]
)
def update_output_div(n_clicks,input_value):
    global speciality
    if input_value:
        my_variable = input_value
        speciality = '@'.join(input_value.split())
        
        my_recruit_df, fig = get_df_n_fig(speciality)

        # mr_json = my_recruit_df.to_json()
        mr_dict = my_recruit_df.to_dict('records')

        if fig:
            return ('선택하신 활동분야는 "{}" 입니다.'.format(my_variable), fig, mr_dict)
    else:
        # _, fig = get_df_n_fig(' ')


        # fig.update_layout(mapbox_style='carto-positron')
        # fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
        # fig = dcc.Graph()
        init = pd.DataFrame(columns=['recruit_id','info_address','lat','lon'], index=[i for i in range(10)]).fillna(0)
        # init_json = init.values()
        init_dict = init.to_dict('records')
        return ['안녕하세요', {}, init_dict]

if __name__ == '__main__':
    app.run_server(debug=True)