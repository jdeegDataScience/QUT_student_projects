# check if any columns contain NA values incorrectly encoded as blank strings, i.e., ''
# returns a list containing the names of columns of interest
def empty_string_values_in_columns(df):
    # empty list to record columns containing blank string values 
    naughty_columns = []

    # check each column
    for col in range(len(df.columns)):
        # store name of current col
        current_col = df.columns[col]
        
        # records if each value in current_col is NOT a blank string
        bools = df[current_col] != ''

        # record current_col if it contains a blank string value
        if not bools.all():
            naughty_columns.append(current_col)
    # there are columns of interest
    if len(naughty_columns) > 0:
        print("Columns to investigate:")
        print(naughty_columns)
    else:
        print("No empty strings found in any columns.")
    return naughty_columns

# programmatically find num_cluster with max silhouette score 
def get_key_by_value(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None  # Return None if the value is not found in the dictionary
