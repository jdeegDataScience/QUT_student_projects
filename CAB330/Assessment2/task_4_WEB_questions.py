# import libraries
import pandas as pd
import numpy as np
from collections import defaultdict
import datetime
from sklearn.linear_model import LinearRegression

# load data
web_data = pd.read_csv('Weblog_v1.csv')

# 1 Load data and preprocess for cluster analysis 
-----------------------
# initialise global vars for preprocessing
session_id = 0
user_id = 0

# create a dictionaries to hold last access information
last_access = defaultdict(lambda:datetime.datetime.utcfromtimestamp(0))
# dictionary to find previous session, user ID
# and steps assigned to a specific date/ip/browser key
session_dict = defaultdict(lambda:1)
user_id_dict = defaultdict(lambda:1)
session_steps = defaultdict(lambda:1)

# preprocess web log data
web_df = preprocess_web_data(df)

# 3 - Data Mining Method: Linear Regression
-----------------------
# generate training data and dependent variable sets
X_lm = web_df.iloc[:, 1:]
y_lm = web_df.iloc[:, 0]

# fit the linear model
web_lm = LinearRegression().fit(X_lm, y_lm)

# create df of features and their coefficient values
coefs = pd.DataFrame(list(zip(web_lm.feature_names_in_, web_lm.coef_)), 
                    columns = ['page', 'coef'])

# filter out features with an predicted effect of less than +/- 1 second
# sort by descending absolute value of coefficient value
coefs = coefs.loc[coefs['coef'].abs() > 1].sort_values(by='coef', key=abs, ascending=False).reset_index(drop=True)

# calculate whole minute approximations for easier interpretation
coefs['minutes'] = (coefs['coef']/60).round(0).astype(int)

# calculate hours approximations for easier interpretation
coefs['hours'] = (coefs['coef']/3600).round(2)

# 4 - Results and Potential Applications
-----------------------
# R^2: Coefficient of Determination
# proportion of variation in Y that is explained by x, i.e. therefor by the model
print(f"The model explains {web_lm.score(X_lm, y_lm):.2%} of the variability in the data")

# display coefs df to discuss results
coefs
