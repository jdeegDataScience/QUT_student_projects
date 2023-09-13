# import pandas as pd
# import numpy as np
# from sklearn.impute import SimpleImputer
def preprocess_all_features(covid_df):
    preprocess_df = covid_df.drop(columns = ['survey_date', 'covid19_positive', 'height', 'weight'])
    preprocess_df = preprocess_df.dropna(subset = ['region', 'country', 'blood_type', 'smoking', 'alcohol', 'contacts_count', 'house_count', 'working'])
    
    # age - label encode with end values to mirror original binning
    preprocess_df.loc[preprocess_df['age'] == '0_10', 'age'] = 9
    preprocess_df.loc[preprocess_df['age'] == '10_20', 'age'] = 19
    preprocess_df.loc[preprocess_df['age'] == '20_30', 'age'] = 29
    preprocess_df.loc[preprocess_df['age'] == '30_40', 'age'] = 39
    preprocess_df.loc[preprocess_df['age'] == '40_50', 'age'] = 49
    preprocess_df.loc[preprocess_df['age'] == '50_60', 'age'] = 59
    preprocess_df.loc[preprocess_df['age'] == '60_70', 'age'] = 69
    preprocess_df.loc[preprocess_df['age'] == '70_80', 'age'] = 79
    preprocess_df.loc[preprocess_df['age'] == '80_90', 'age'] = 89
    preprocess_df.loc[preprocess_df['age'] == '90_100', 'age'] = 99
    preprocess_df.loc[preprocess_df['age'] == '100_110', 'age'] = 109
    preprocess_df['age'] = preprocess_df['age'].astype('int64')
    
    # insurance - imputation: bfill
    preprocess_df.loc[preprocess_df['insurance'] == 'yes', 'insurance'] = 1
    preprocess_df.loc[preprocess_df['insurance'] == 'no', 'insurance'] = 0
    preprocess_df.loc[preprocess_df['insurance'] == 'blank', 'insurance'] = np.nan
    preprocess_df['insurance'] = preprocess_df['insurance'].bfill()    
    
    # income - imputation: bfill
    # drop gov (90)
    preprocess_df = preprocess_df[preprocess_df['income'] != 'gov']
    # ordinal encode
    preprocess_df.loc[preprocess_df['income'] == 'low', 'income'] = 0
    preprocess_df.loc[preprocess_df['income'] == 'med', 'income'] = 1
    preprocess_df.loc[preprocess_df['income'] == 'high', 'income'] = 2
    preprocess_df.loc[preprocess_df['income'] == 'blank', 'income'] = np.nan # (108)
    # fill NAs
    preprocess_df['income'] = preprocess_df['income'].bfill()
    
    # race - drop blank (18) ; imputation: bfill
    preprocess_df = preprocess_df[preprocess_df['race'] != 'blank']
    # bfill NAs
    preprocess_df['race'] = preprocess_df['race'].bfill()
    
    # immigrant: 0.121 immigrant, 0.869 native, 0.010 NA ; ref encode 0 = native, 1 = immigrant, impute NA with bfill
    preprocess_df.loc[preprocess_df['immigrant'] == 'native', 'immigrant'] = 0
    preprocess_df.loc[preprocess_df['immigrant'] == 'immigrant', 'immigrant'] = 1
    preprocess_df.loc[preprocess_df['immigrant'] == 'blank', 'immigrant'] = np.nan
    # impute missing values
    preprocess_df['immigrant'] = preprocess_df['immigrant'].bfill()
    
    # smoking - ref encode nonsmokers to new var and...
    preprocess_df.loc[preprocess_df['smoking'] == 'never', 'never_smoked'] = 1
    preprocess_df.loc[preprocess_df['smoking'] != 'never', 'never_smoked'] = 0
    # ...ref encode vape to new var and...
    preprocess_df.loc[preprocess_df['smoking'] == 'vape', 'vape'] = 1
    preprocess_df.loc[preprocess_df['smoking'] != 'vape', 'vape'] = 0
    # ...label encode ex/smokers to separate vars
    ex_smoker_conditions = [(preprocess_df['smoking'].eq("quit0")), (preprocess_df['smoking'].eq("quit5")), (preprocess_df['smoking'].eq("quit10"))]
    smoker_conditions = [(preprocess_df['smoking'].eq("yeslight")), (preprocess_df['smoking'].eq("yesmedium")), (preprocess_df['smoking'].eq("yesheavy"))]
    smoking_choices = [1, 2, 3]
    preprocess_df["ex_smoker"] = np.select(ex_smoker_conditions, smoking_choices)
    preprocess_df["smoker"] = np.select(smoker_conditions, smoking_choices)
    preprocess_df = preprocess_df.drop(columns = ['smoking'])
    
    # alcohol - correct x<1 to 0, drop missing values (30)
    # denote errorneous values in alcohol
    alcohol_mask = preprocess_df['alcohol'] < 1
    # loc can replace erroneous values
    preprocess_df.loc[alcohol_mask, 'alcohol'] = 0
    
    # imputer for imputation with mode
    mode_imputer = SimpleImputer(strategy="most_frequent")    
    # cannabis - correct x<1 to 0, fill missing values 
    # denote errorneous values in cannabis
    cannabis_mask = preprocess_df['cannabis'] < 1
    # loc can replace erroneous values
    preprocess_df.loc[cannabis_mask, 'cannabis'] = 0
    # impute missing values in cannabis with mode value ; 0
    preprocess_df['cannabis'] = mode_imputer.fit_transform(preprocess_df['cannabis'].values.reshape(-1,1))
    
    # amphetamines - correct x<1 to 0, fill missing values 
    # denote errorneous values in amphetamines
    amphetamines_mask = preprocess_df['amphetamines'] < 1
    # loc can replace erroneous values
    preprocess_df.loc[amphetamines_mask, 'amphetamines'] = 0
    # impute missing values in amphetamines with mode value ; 0
    preprocess_df['amphetamines'] = mode_imputer.fit_transform(preprocess_df['amphetamines'].values.reshape(-1,1))
    
    # cocaine - correct x<1 to 0, fill missing values 
    # denote errorneous values in cocaine
    cocaine_mask = preprocess_df['cocaine'] < 1
    # loc can replace erroneous values
    preprocess_df.loc[cocaine_mask, 'cocaine'] = 0
    # impute missing values in cocaine with mode value ; 0
    preprocess_df['cocaine'] = mode_imputer.fit_transform(preprocess_df['cocaine'].values.reshape(-1,1))    
    
    # public_transport_count - fill NAs with 0
    preprocess_df['public_transport_count'] = preprocess_df['public_transport_count'].fillna(0)
    
    # working - never_employed = never ; work_stopped = stopped ; # WFH = home ; working_travel = non crit = 0, crit = 1 ; drop parent 'working' column
    # never_employed
    preprocess_df.loc[preprocess_df['working'] == 'never', 'never_employed'] = 1
    preprocess_df.loc[preprocess_df['working'] != 'never', 'never_employed'] = 0
    # work_stopped
    preprocess_df.loc[preprocess_df['working'] == 'stopped', 'work_stopped'] = 1
    preprocess_df.loc[preprocess_df['working'] != 'stopped', 'work_stopped'] = 0
    # WFH
    preprocess_df.loc[preprocess_df['working'] == 'home', 'WFH'] = 1
    preprocess_df.loc[preprocess_df['working'] != 'home', 'WFH'] = 0
    # working_travel
    preprocess_df.loc[preprocess_df['working'] == 'travel critical', 'working_travel'] = 1  # 2
    preprocess_df.loc[preprocess_df['working'] == 'travel non critical', 'working_travel'] = 0 # 1
    # preprocess_df.loc[(preprocess_df['working'] != 'travel non critical') | (preprocess_df['working'] != 'travel critical'), 'working_travel'] = 0
    # drop original column
    preprocess_df = preprocess_df.drop(columns = ['working'])
    
    # imputer for imputation with mean
    mean_imputer = SimpleImputer(strategy="mean")
    # worried - fill NAs with (rounded) mean
    # preprocess_df['worried'] = preprocess_df['worried'].fillna(preprocess_df['worried'].mean(), inplace=True)
    preprocess_df['worried'] = mean_imputer.fit_transform(preprocess_df['worried'].values.reshape(-1,1))
    preprocess_df['worried'] = preprocess_df['worried'].round(0)
    
    # one-hot encoding
    preprocess_df = pd.get_dummies(preprocess_df)
    
    # ensure risk_infection is int64
    preprocess_df['risk_infection'] = preprocess_df['risk_infection'].astype('int64')
    
    return preprocess_df
