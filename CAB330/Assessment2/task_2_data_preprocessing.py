# import pandas as pd
# import numpy as np

def preprocess_pos_data(raw_pos_data):
    # drop duplicates
    preprocess_df = raw_pos_data.drop_duplicates()
    
    # replace blank strings with nan
    preprocess_df['Transaction_Id'] = preprocess_df['Transaction_Id'].replace('', np.nan)
    preprocess_df['Quantity'] = preprocess_df['Quantity'].replace('', np.nan)

    # drop rows containing nan's
    preprocess_df.dropna(inplace = True)
    
    # drop unnecessary features
    preprocess_df.drop(columns = ['Location', 'Transaction_Date', 'Quantity'], inplace = True)
    
    # typecast as needed
    preprocess_df['Product_Name'] = preprocess_df['Product_Name'].astype(str)
    preprocess_df['Transaction_Id'] = preprocess_df['Transaction_Id'].astype(int)
    
    # reset index
    preprocess_df.reset_index(drop=True, inplace=True)
    
    return preprocess_df
