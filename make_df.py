import pandas as pd

def get_dataframe(idxs, lat_lon_df):

    df = pd.DataFrame(idxs, columns=['recruit_id'])

    my_recruit_df = pd.merge(left=df, right=lat_lon_df, how='left', on='recruit_id')
    my_recruit_df['info_address'].fillna('재택', inplace=True)
    my_recruit_df.fillna(0, inplace=True)
    my_recruit_df['lat'] = my_recruit_df['lat'].apply(lambda x : round(x,4))
    my_recruit_df['lon'] = my_recruit_df['lon'].apply(lambda x : round(x,4))

    map_df = my_recruit_df[my_recruit_df['lat'] != 0]

    return map_df, my_recruit_df