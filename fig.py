import plotly.express as px
import pandas as pd
from sim import simirality_df, Similarity
from make_df import get_dataframe


def get_df_n_fig(speciality):

    lat_lon_df = pd.read_csv('./lat_lon_df.csv', sep=';')
    sim = Similarity(simirality_df, 'ehddnr', speciality, 'cosine')

    idxs = sim.get_item()

    map_df, my_recruit_df = get_dataframe(idxs, lat_lon_df)
    print(my_recruit_df)
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

    return my_recruit_df, fig