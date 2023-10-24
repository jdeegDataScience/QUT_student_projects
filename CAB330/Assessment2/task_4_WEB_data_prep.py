# import pandas as pd

def preprocess_web_data(raw_web_data):
    # drop duplicates
    preprocess_df = raw_web_data.drop_duplicates()
    
    # rename columns
    preprocess_df = preprocess_df.rename(columns = {'IP address' : 'ip', 'Timestamp' : 'time',
                                                    'Request' : 'request', 'Staus' : 'status'})
    
    # remove all unsuccessful requests (code != 200)
    preprocess_df = preprocess_df[preprocess_df['status'] == 200]
    
    # remove leading square bracket from timestamp
    preprocess_df['time'] = preprocess_df['time'].str.replace('[', '')
    
    # convert to datetime 
    preprocess_df['time'] = pd.to_datetime(preprocess_df['time'], format= '%d/%b/%Y:%H:%M:%S')
    
    # remove useless " HTTP/1.1" and " HTTP/1.0" from request strings
    preprocess_df['request'] = preprocess_df['request'].str.slice(start=0, stop=-9)    
    
    # extract usernames
    usernames = preprocess_df['request'].str.extractall('.+nm=([\w]+)|\?user=([\w]+)|\?name=([\w]+)|show=([\w]+)')
    usernames = usernames.fillna('')
    usernames['username'] = usernames[0] + usernames[1] + usernames[2]
    usernames['UN_shown'] = usernames[3]
    usernames = usernames[['username', 'UN_shown']].droplevel(level=1)
    preprocess_df = preprocess_df.merge(usernames, left_index=True, right_index=True, how='left')
    
    # convert empty values back to NAs
    preprocess_df['UN_shown'] = preprocess_df['UN_shown'].replace('', np.nan).astype(object)
    preprocess_df['username'] = preprocess_df['username'].replace('', np.nan).astype(object)
    
    # parse method from requests
    preprocess_df['method'] = preprocess_df['request'].str.split(' ',expand=True)[0]
    
    # reset index
    preprocess_df.reset_index(drop=True, inplace=True)
    
    return preprocess_df