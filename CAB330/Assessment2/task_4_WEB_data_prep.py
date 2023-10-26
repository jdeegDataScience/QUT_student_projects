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
    
    # extract usernames
    usernames = preprocess_df['request'].str.extractall('.+nm=([\w]+)|\?user=([\w]+)|\?name=([\w]+)|show=([\w]+)')
    usernames = usernames.fillna('')
    usernames['username'] = usernames[0] + usernames[1] + usernames[2] + usernames[3]
    usernames = usernames['username'].droplevel(level=1)
    preprocess_df = preprocess_df.merge(usernames, left_index=True, right_index=True, how='left')
    
    # convert empty values back to NAs
    preprocess_df['username'] = preprocess_df['username'].replace('', np.nan).astype(object)
    
    # parse pages from requests
    request_splits = preprocess_df['request'].str.split(expand=True)
    preprocess_df['page'] = request_splits[1].str.extract('/(.*)\.php')
    
    # drop request column
    preprocess_df.drop(columns='request', inplace=True)

    # apply function above to get a new dataframe with added information
    web_sessions = preprocess_df.apply(get_log_user_info, axis=1)

    # Drop rows where 'page' is NaN
    web_sessions = web_sessions.dropna(subset=['page'])
    
    # Add 'sessionLength' column
    web_sessions['sessionLength'] = web_sessions.groupby('session')['time'].apply(lambda x: (x.max() - x.min()).seconds)
    # Drop rows where 'sessionLength' is NaN
    web_sessions.dropna(subset=['sessionLength'], inplace=True)
    # Filter and drop rows where 'sessionLength' is less than 1 (Bot traffic)
    web_sessions = web_sessions[web_sessions['sessionLength'] >= 1]
    
    web_sessions = pd.get_dummies(web_sessions, columns=['page'], prefix=[''], prefix_sep=[''])
    
    web_sessions = web_sessions.groupby('session').last().reset_index()
    
    # return only the required columns
    return web_sessions.iloc[:,7:]



def get_log_user_info(row):
    # access global variables shared between all rows
    global session_id, user_id, session_dict, user_id_dict, session_steps, last_access
    
    # date + IP key for finding session
    session_key = str(row['time'].date()) + '_' + row['ip']
    
    # date + IP + browser key for finding user
    user_key = str(row['time'].date()) + '_' + row['ip'] + '_' + str(row['username'])
    
    # session time diff
    time_diff_session = row['time'] - last_access[session_key]  
    
    # user time diff
    time_diff_user = row['time'] - last_access[user_key]  
    
    # if the time diff from previous session is > 30 mins, assign new session ID
    if time_diff_session.total_seconds() > 1800:
        session_id += 1
        session_dict[session_key] = session_id
    
    # if the time diff from previous session is > 60 mins, assign new user ID
    if time_diff_user.total_seconds() > 3600:
        user_id += 1
        user_id_dict[user_key] = user_id
        
    # update last access for session and user
    last_access[session_key] = row['time']
    last_access[user_key] = row['time']
    
    # assign extracted info from the row
    row['session'] = session_dict[session_key]
    row['step'] = session_steps[row['session']]
    row['userID'] = user_id_dict[user_key]
    session_steps[row['session']] += 1
    return row
