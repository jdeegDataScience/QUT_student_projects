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

    # apply function above to get a new dataframe with added information
    web_sessions = preprocess_df.apply(get_log_user_info, axis=1)

    web_sessions_enriched = session_clustering_enrichment(web_sessions)
    
    return web_sessions_enriched

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

def session_clustering_enrichment(web_sessions):
    # Create session_request_counts DataFrame
    session_request_counts = web_sessions.groupby('session')['request'].nunique().reset_index()
    session_request_counts.rename(columns={'request': 'requests_per_session'}, inplace=True)
    
    # Assuming session_request_counts has columns: ['sessionLength', 'requests_per_session', 'isLoggedIn', 'UserID', 'IP Address']
    columns_to_plot = ['sessionLength', 'requests_per_session', 'isLoggedIn', 'userID', 'returnUser']
    
    # Add the 'Username' column to session_request_counts
    session_request_counts['username'] = web_sessions.groupby('session')['username'].last().values
    # Fill NaN values in the 'Username' column with a default value
    session_request_counts['username'].fillna('Guest', inplace=True)
    # Create a binary variable indicating whether the user was isLoggedIn
    session_request_counts['isLoggedIn'] = session_request_counts['username'] != 'Guest'
    
    # Add 'IP Address' column
    session_request_counts['ip'] = web_sessions.groupby('session')['ip'].last().values
    # Identify returnUser based on matching IP addresses
    session_request_counts['returnUser'] = session_request_counts.duplicated(subset='ip', keep='first')
    
    # Add 'method' column to session_request_counts
    session_request_counts['method'] = web_sessions.groupby('session')['method'].last().values
    
    # Add 'userID' column to session_request_counts
    session_request_counts['userID'] = web_sessions.groupby('session')['userID'].last().values
    
    # Add 'sessionLength' column
    session_request_counts['sessionLength'] = web_sessions.groupby('session')['time'].apply(lambda x: (x.max() - x.min()).seconds)
    # Drop rows where 'sessionLength' is NaN
    session_request_counts = session_request_counts.dropna(subset=['sessionLength'])
    
    # Extract features for clustering
    features_for_clustering = session_request_counts[columns_to_plot]

    return features_for_clustering
