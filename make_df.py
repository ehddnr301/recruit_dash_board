import pandas as pd

df1 = pd.read_csv('/Users/don/Documents/similarity/data/add_reco_count.csv', sep=';').drop(columns=['class', 'info_address'], axis=1)
df2 = pd.read_csv('/Users/don/Documents/similarity/data/role_specialty.csv', sep=';').drop(columns=['class'], axis=1)
df3 = pd.read_csv('/Users/don/Documents/similarity/data/title_income_career.csv', sep=';').drop(columns=['class', 'main_response', 'main_view_count'], axis=1)

def get_dataframe(idxs, lat_lon_df):

    df = pd.DataFrame(idxs, columns=['recruit_id'])

    my_recruit_df = pd.merge(left=df, right=lat_lon_df, how='left', on='recruit_id')
    my_recruit_df['info_address'].fillna('재택', inplace=True)
    my_recruit_df.fillna(0, inplace=True)
    my_recruit_df['lat'] = my_recruit_df['lat'].apply(lambda x : round(x,4))
    my_recruit_df['lon'] = my_recruit_df['lon'].apply(lambda x : round(x,4))

    map_df = my_recruit_df[my_recruit_df['lat'] != 0]

    my_recruit_df = pd.merge(left=my_recruit_df, right=df1, how='left', on='recruit_id')
    my_recruit_df = pd.merge(left=my_recruit_df, right=df2, how='left', on='recruit_id')
    my_recruit_df = pd.merge(left=my_recruit_df, right=df3, how='left', on='recruit_id')
    my_recruit_df.drop(columns=['info_address', 'lat', 'lon'], inplace=True)
    my_recruit_df.rename(columns={'recruit_id': '공고번호', 'main_recruit_title': '공고명', 'main_income': '연봉정보', 'main_need_career': '경력요구사항'}, inplace=True)

    return map_df, my_recruit_df