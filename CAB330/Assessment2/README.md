This can act as a centralised 'summary document' for our considerations and decisions throughout the completion of Case Study 2.

# Task 1: Clustering

## Data Prep Notes

### Features
- ID: PK; drop, not useful
- Name: Arbitrary, unique 86% records. Drop, not useful.
- Energy
    - dType & allowable values: float, 0 to 1.
    - Found 1 record with invalid blank string value, replaced with NaN as in wk9 prac.
- Loudness
    - dType & allowable values: float, 0 to 1.
    - Standardization should of this feature should improve model performance. 
    - Found 1 record with invalid blank string value, replaced with NaN as in wk9 prac.
- Speechiness
    - trial log transformation
        - *improved output?*
    - Binary encode? based on info from assignment instructions.
        - `preprocess_df.loc[preprocess_df['Speechiness'] > 0.65, 'spoken_word_only'] = 1`
        - `preprocess_df.loc[preprocess_df['Speechiness'] < 0.65, 'spoken_word_only'] = 0`
            - eg. talk shows, podcasts, audiobooks, etc...
        - *improved output?*
- Instrumentalness
    - perhaps should be binary encoded? Same threshold as *Speechiness*, i.e., greater than 0.65 is an instrumental track.
        - `preprocess_df.loc[preprocess_df['Instrumentalness'] > 0.65, 'instrumental'] = 1`
        - `preprocess_df.loc[preprocess_df['Instrumentalness'] < 0.65, 'instrumental'] = 0`
        - *improved output?*
    - Found 1 record with invalid blank string value, replaced with NaN as in wk9 prac.
- Type: Same for every record, dropped.
- time_signature
    - Not sure what to make of 0 and 1 values, does not make sense in a musical context.
    - Singular `0` value is very suspicious.
    - Distinct value counts:
        - 5 : 88
        - 4 : 2547
        - 3 : 305
        - 2 : 0
        - 1 : 39
        - 0 : 1

### Preprocessing Steps
1. Drop Duplicate Records
    1. Drops 292 duplicate records; confirm number duplicate records `music_data.duplicated().value_counts()`
1. Replace Blank String Values & Convert Data Types
    1. Blank string values in *Energy*, *Loudness*, and *Instrumentalness* replaced with `NaN` and converted to `float`.
1. Drop NaNs in *Energy*, *Loudness*, and *Instrumentalness*
1. Drop Records with Invalid Values
    1. Drops records with values beyond permissible range (0 to 1) in *Energy*, *Speechiness*, or *Instrumentalness*.
    1. Creates temporary column *drop_col*
1. Drop Unnecessary Features
    1. *ID* as it is Primary Key, not useful for clustering
    1. *Type* as it contains same value for every record
    1. *Name* as it is unique for 86% of records, not useful for clustering
    1. *drop_col* as it has served it's purpose
1. Reset Index
    1. Previous index values are not useful, clean slate is best practice and precludes and referencing errors in subsequent data operations.

# Task 2: Association Mining
## Data Prep Notes
- Data is long; 1 row per item in every transaction.

### Features
- Location ***Drop***
- Transaction_Id
    - 199999 unqiue transaction ID's
    - 2 rows with blank strings values
    - Transaction_Id are unique across all locations
- Transaction_Date ***Drop***
- Product_Name
    - 17 unqiue products
    - 0 rows with blank strings values
- Quantity
    - 2 rows with invalid blank string values
    - Keep to drop records with invalid values *then* **drop**

### Preprocessing Steps
1. Drop duplicates
    1. Affects 169044 records
    1. Do not need to include same item in same transaction more than once
    1. AFAIK does not affect Association Analysis
1. Replace blank string values with `np.nan`
    1. `Transaction_Id` and `Quantity` 
    1. Affects 4 records
1. Drop NaN rows
    1. Affects 4 records
    1. Investigated and found that these seemed to be 'corrupted' duplicates of other records.
1. Drop Unnecessary Features
    1. `Location`, `Transaction_Date` and `Quantity`
        1. `Quantity` of item per transaction is not of interest, only presence of item in transaction.
1. Typecast as need
    1. `Transaction_Id` to `int`
    1. `Product_Name` to `str`
1. Reset Index
    1. Previous index values are not useful, clean slate is best practice and precludes and referencing errors in subsequent data operations.

# Task 3: Text Analysis
## Data Prep Notes
### Preprocessing Steps
1. Drop all columns except `Description`
1. If `optimise` is `False` == Default Text Analysis
    1. `stopwords` are set to the default English stopwords.
    1. Token vector initialised `cab_tokenizer`, `ngram_range=(1,2)` and otherwise default parameters
1. Else `optimise` = `True` == More data massaging & filtered token vector
    1. `stopwords` are set to the default English stopwords and additional selected frequent tokens that were deemed not useful.
    1. Strip identified noisy string patterns from data; "*. -- (C) Official Site*" etc...
    1. Token vector initialised using `cab_tokenizer`, `ngram_range=(1,2)`, `min_df=40`, `max_df=0.7` and otherwise default parameters.
1. Generate Document-Matrix
1. Return Token Vector and Document-Term Matrix

# Task 4: Web Log Mining
## Data Prep Notes
### Preprocessing Steps
1. Drop Duplicates (2169)
1. Rename Columns
    1. `{'IP address' : 'ip', 'Timestamp' : 'time', 'Request' : 'request', 'Staus' : 'status'}`
1. Drop Unsuccessful Requests (3522)
1. Strip leading `[` from DateTime column
1. Convert column to DateTime
1. Trim Unnecessary Chars from `request` Column
    1. `' HTTP/1.1'` and `' HTTP/1.0'`
1. Extract Usernames from `requests`
    1. `'.+nm=([\w]+)|\?user=([\w]+)|\?name=([\w]+)|show=([\w]+)'`
    1. `nm`, `name`, and `user` are combined into a new column `username`
    1. `show` values are stored in a different column, `UN_shown`
1. Extract `method` from `request`
1. Reset Index
    1. Previous index values are not useful, clean slate is best practice and precludes and referencing errors in subsequent data operations.
