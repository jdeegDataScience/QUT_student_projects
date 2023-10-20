# import pandas as pd
# import numpy as np

def preprocess_music_data(raw_music_data):
    # drop duplicate rows 
    preprocess_df = raw_music_data.drop_duplicates()
    
    # replace blank strings with NaN, typecast to float
    preprocess_df['Energy'] = preprocess_df['Energy'].replace('', np.nan).astype(float)
    preprocess_df['Loudness'] = preprocess_df['Loudness'].replace('', np.nan).astype(float)
    preprocess_df['Instrumentalness'] = preprocess_df['Instrumentalness'].replace('', np.nan).astype(float)
    
    # drop outliers / beyond permissible range
    # map invalid values
    preprocess_df.loc[preprocess_df['Energy'] > 1, 'drop_col'] = True
    preprocess_df.loc[preprocess_df['Instrumentalness'] > 1, 'drop_col'] = True
    preprocess_df.loc[preprocess_df['Speechiness'] > 1, 'drop_col'] = True
    # drop from df
    preprocess_df = preprocess_df[preprocess_df.drop_col != True]
    
    # drop unnecessary features
    preprocess_df = preprocess_df.drop(columns = ['ID', 'Type', 'Name', 'drop_col'])
    
    # reset index
    preprocess_df.reset_index(drop=True, inplace=True)
    
    return preprocess_df
