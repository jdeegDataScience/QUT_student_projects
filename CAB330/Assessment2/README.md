This can act as a centralised 'summary document' for our considerations and decisions throughout the completion of Case Study 2.

# Task 1: Clustering

## Data Prep Notes

### Features
- **TBC** potential inverse corr. b/w *Speechiness* and *Instrumentalness*; low speechiness *should* indicate high instrumentalness?

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
    - potentially log transform for more gaussian distribution?
    - helps with range, but may not be an important attribute when it come to find similarity and disimilarities.
    - perhaps should be binned or encoded? Suggestions based on info from assignment instructions.
        - *\>=0.66* = T/F or 0/1 for *spoken_word_only*, eg. talk shows, podcasts, audiobooks, etc...
        - *\<0.66 & \<=0.33* = music with words?
        - *\<0.33* = instrumental/music only?
- Instrumentalness
    - perhaps should be binary encoded? Greater than 0.5 to 'True', i.e. it is an instrumental track.
    - Found 1 record with invalid blank string value, replaced with NaN as in wk9 prac.
- Type: Same for every record, dropped.
- time_signature
    - not sure what to make of 0 and 1 values, does not make sense in a musical context.
    - Distinct value counts:
        - 4 : 2547
        - 3 : 305
        - 5 : 88
        - 1 : 39
        - 0 : 1

# Task 2: Association Mining
## Data Prep Notes
- Data is long; 1 row per item in transaction

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
