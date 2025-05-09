import pyodbc
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report


# Open a connection to SQL Server COVID19_Survey database
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=COVID19_Survey;"
    "Trusted_Connection=yes;"
)

# Write query that joins Fact_survey to Participant to Response and selects only the numeric & bool/bit columns plus the two targets
# boolean/bit flags are cast as INT so that pandas sees them as numeric
sql = """
SELECT
  fs.Risk_infection,
  fs.Covid19_positive,

  p.Height,
  p.Weight,
  p.Bmi,

  r.Contact_count,
  r.House_count,
  r.Public_transport_count,

  CAST(r.Covid19_symptoms AS INT) AS Covid19_symptoms,
  CAST(r.Covid19_contact  AS INT) AS Covid19_contact,
  CAST(r.Asthma AS INT) AS Asthma,
  CAST(r.Kidney_disease AS INT) AS Kidney_disease,
  CAST(r.Liver_disease AS INT) AS Liver_disease,
  CAST(r.Compromised_immune AS INT) AS Compromised_immune,
  CAST(r.Heart_disease AS INT) AS Heart_disease,
  CAST(r.Lung_disease AS INT) AS Lung_disease,
  CAST(r.Diabetes AS INT) AS Diabetes,
  CAST(r.Hiv_positive AS INT) AS Hiv_positive,
  CAST(r.Hypertension AS INT) AS Hypertension,
  CAST(r.Other_chronic AS INT) AS Other_chronic,
  CAST(r.Nursing_home AS INT) AS Nursing_home,
  CAST(r.Health_worker AS INT) AS Health_worker
FROM dbo.Fact_survey AS fs
JOIN dbo.Participant AS p
  ON fs.Participant = p.Participant_ID
JOIN dbo.Response AS r
  ON fs.Response = r.Response_ID
WHERE fs.Risk_infection IS NOT NULL
  AND fs.Covid19_positive IS NOT NULL;
"""

# Load into DataFrame
df_covid19 = pd.read_sql(sql, conn)
conn.close()

# Compute correlation of every column against Risk_infection
corr_riskinfection = df_covid19.corr()["Risk_infection"].drop("Risk_infection")

# Compute correlation against Covid19_positive
corr_positive = df_covid19.corr()["Covid19_positive"].drop("Covid19_positive")

# Combine into one table
corr_df = pd.DataFrame({
    "corr_riskinfection": corr_riskinfection,
    "corr_positive": corr_positive
}).sort_values(by="corr_riskinfection", ascending=False)

print(corr_df)

# Split features and target
X = df_covid19.drop(columns=['Risk_infection'])
y = df_covid19['Risk_infection']

# Define number of features to select
k = 10

# ANOVA (f_regression)
selector_f = SelectKBest(score_func=f_regression, k=k)
selector_f.fit(X, y)
scores_f = pd.Series(selector_f.scores_, index=X.columns).sort_values(ascending=False)
selected_f = list(scores_f.head(k).index)

# Mutual Info
selector_m = SelectKBest(score_func=mutual_info_regression, k=k)
selector_m.fit(X, y)
scores_m = pd.Series(selector_m.scores_, index=X.columns).sort_values(ascending=False)
selected_m = list(scores_m.head(k).index)

# Display results in a DataFrame
result = pd.DataFrame({
    'ANOVA Score': scores_f,
    'Mutual Info Score': scores_m
})

print("Top {} features by ANOVA:".format(k), selected_f)
print("Top {} features by Mutual Information:".format(k), selected_m)

# Split out 20% for model testing 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the decision tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
y_dt = dt.predict(X_test)
acc_dt = accuracy_score(y_test, y_dt)

# Train the GNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_gnb = gnb.predict(X_test)
acc_gnb = accuracy_score(y_test, y_gnb)

# Output results
print(f"Decision Tree Accuracy: {acc_dt:.3f}")
print(classification_report(y_test, y_dt, zero_division=0))

print(f"GaussianNB Accuracy:     {acc_gnb:.3f}")
print(classification_report(y_test, y_gnb, zero_division=0))
