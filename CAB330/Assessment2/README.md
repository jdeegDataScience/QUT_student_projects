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
        - 4 : 2547
        - 3 : 305
        - 5 : 88
        - 1 : 39
        - 0 : 1

### Preprocessing Steps
- Drop Duplicate Records
    - Drops 292 duplicate records; confirm number duplicate records `music_data.duplicated().value_counts()`
- Replace Blank String Values & Convert Data Types
    - Blank string values in *Energy*, *Loudness*, and *Instrumentalness* replaced with `NaN` and converted to `float`.
- Drop Records with Invalid Values
    - Drops records with values beyond permissible range (0 to 1) in *Energy*, *Speechiness*, or *Instrumentalness*.
    - Creates temporary column *drop_col*
- Drop Unnecessary Features
    - *ID* as it is Primary Key, not useful for clustering
    - *Type* as it contains same value for every record
    - *Name* as it is unique for 86% of records, not useful for clustering
    - *drop_col* as it has served it's purpose
- Reset Index
    - previous index values are not useful, clean slate is best practice and precludes and referencing errors in subsequent data operations.

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
- Drop `Location` and `Transaction_Date`
- Replace blank string values in `Transaction_Id` and `Quantity` with `NaN`
    - Affects 4 records
- Drop NaN rows
    - Affects 4 records
- Drop `Quantity`
- Typecast as need
    - `Transaction_Id` to `int`
    - `Product_Name` to `str`
- Drop duplicates
    - Affects 169044 records
    - Do not need to include same item in same transaction more than once
    - AFAIK does not affect Association Analysis
