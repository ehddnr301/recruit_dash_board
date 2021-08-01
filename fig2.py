from typing_extensions import final
import plotly.express as px
import pandas as pd
from w2v_sim import W2VSimilarity, final_df
from make_df import get_dataframe


def get_df_n_fig2(text):
    lat_lon_df = pd.read_csv('./lat_lon_df.csv', sep=';')
    sim = W2VSimilarity(final_df, 'ehddnr', text)

    df = sim.get_item()

    idxs = list(df['recruit_id'].values)

    map_df, my_recruit_df = get_dataframe(idxs, lat_lon_df)

    my_recruit_df = my_recruit_df.rename(columns={col : f'{col} ' for col in my_recruit_df.columns} )

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

