# import libraries and packages
import warnings
warnings.filterwarnings('ignore')
import pyodbc
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests

from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# define var for random state to ensure reproducibility 
rs = 42

# CHECK PACKAGE VERSIONS --- plotting will break if versions are not correct & compatible
pd.__version__ # expected: 2.2.3
matplotlib.__version__ # expected: 3.9.4
sns.__version__ # expected: 0.13.2
np.__version__ # expected: 1.23.0

# function definitions to import data set and perform feature selection 

def import_sql_db_COVID19_Survey(pd, pyodbc):
    # Open a connection to SQL Server COVID19_Survey database
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=COVID19_Survey;"
        "Trusted_Connection=yes;"
    )

    # Write query that joins Fact_survey to Participant to Response
    # and selects only the numeric & bool/bit columns plus the two targets
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
    df = pd.read_sql(sql, conn)
    conn.close()
    
    return df

def compare_feat_selectors(X, y, num_features, feat_select_score_funcs, packages_arr, classifier_names=["Decision Tree", "Gaussian Naive Bayes"], rs=42):
    # vars to store feature selection results
    top_sel_feats = pd.DataFrame(dtype='S')
    scores_df = pd.DataFrame(index=X.columns.sort_values())
    
    # loop score functions
    for i in range(len(feat_select_score_funcs)):
        np.random.seed(rs)  # where not explicitly supplied, reset rng seed before each use
        # fit selector
        selector = SelectKBest(score_func=feat_select_score_funcs[i][1], k=num_features).fit(X, y)
        
        # extract + store scores, feature names
        func_scores = pd.Series(selector.scores_, index=selector.feature_names_in_, name="attribute").sort_index()
        scores_df[feat_select_score_funcs[i][0]] = func_scores
        top_sel_feats[feat_select_score_funcs[i][0]] = func_scores.nlargest(n=num_features, keep='all').index.to_list()
    
    # df to store model fit results
    model_accuracies = pd.DataFrame(columns=['accuracy', 'dataset', 'selector', 'classifier'])
    
    # loop features:classifiers
    for col in top_sel_feats.columns:
        # Re‐slice X to selected features of curr scoring func 
        X_sel = X[top_sel_feats[col].tolist()]
        
        # Split out 20% for model testing 
        X_train, X_test, y_train, y_test = train_test_split(X_sel, y, test_size=0.2, random_state=rs)
        
        # Train the decision tree
        dt = DecisionTreeClassifier(random_state=rs)
        dt.fit(X_train, y_train)
        
        dt_accuracy = pd.DataFrame({'accuracy':[dt.score(X_train, y_train), dt.score(X_test, y_test)],
                                    'dataset':["training", "test"], 'selector': col, 'classifier':[classifier_names[0], classifier_names[0]]})
        model_accuracies = pd.concat([model_accuracies, dt_accuracy], ignore_index=True)
        
        # Train the GNB
        gnb = GaussianNB()
        gnb.fit(X_train, y_train)
        gnb_accuracy = pd.DataFrame({'accuracy':[gnb.score(X_train, y_train), gnb.score(X_test, y_test)],
                                     'dataset':["training", "test"], 'selector': col, 'classifier':[classifier_names[1], classifier_names[1]]})
        model_accuracies = pd.concat([model_accuracies, gnb_accuracy], ignore_index=True)
    
    scores_df.reset_index(inplace=True)
    scores_df.rename({'index':'Attribute'}, axis=1, inplace=True)
    
    return top_sel_feats, scores_df, model_accuracies

# retrieve data 
df_covid19 = import_sql_db_COVID19_Survey()

# --- ------ ---
# --- Task 1 ---
# --- ------ ---

# --- Correlations ---
# Compute correlation of every column against Risk_infection
corr_riskinfection = df_covid19.corr()["Risk_infection"].drop("Risk_infection")

# Compute correlation against Covid19_positive
corr_positive = df_covid19.corr()["Covid19_positive"].drop("Covid19_positive")

# Combine into one table
corr_df = pd.DataFrame({
    "corr_riskinfection": corr_riskinfection,
    "corr_positive": corr_positive}).sort_values(by="corr_riskinfection")

# print corrs; reverse sort order for output
print(corr_df.sort_values(by="corr_riskinfection", ascending=False))

# uncomment if you want to export the corelation values to a csv
# corr_df.sort_values(by="corr_riskinfection", ascending=False).to_csv("./attr_corrs.csv", index_label="attribute")

# prep data and consts for plotting
sort_positive = "corr_positive"
sort_infctn = "corr_riskinfection"
corr_df_plt = corr_df.dropna().sort_values(by=sort_infctn) # use the other sort_ var to alter attribute order in plots
titles = ["Covid Infection Risk", "Covid Positive"]

# plot correlations
fig, axes = plt.subplots(figsize=(16,7), ncols=2, sharey=True, layout='constrained')
norm = plt.Normalize(vmin=-1, vmax=1)
cmap = plt.cm.get_cmap('coolwarm')
# add titles and correct colormap range to axes 
for i in range(len(corr_df_plt.columns)):
    col = corr_df_plt.columns[i]    
    axes[i].set_title(titles[i], fontstyle='italic')
    axes[i].set_xlim(-0.3, 0.5)
    axes[i].grid(axis='x')
    for j, value in enumerate(corr_df_plt[col]):
        color = cmap(norm(value))
        axes[i].barh(corr_df_plt.index[j], value, color=color, zorder=2) 
# add colorbar to figure
cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='coolwarm', norm=norm), cax=axes[1].inset_axes([1.05, 0.1, 0.05, 0.8]))
cbar.set_label("Correlation Value", rotation=270, labelpad=10)
plt.suptitle('Attribute correlations with Target Attribute...', size='x-large',  y = 1.03)

# --- ------ ---
# --- Task 2 ---
# --- ------ ---

# --- Feature Selection ---
# iterable object for feature select score functions
score_functions = pd.Series([["ANOVA", f_classif], 
                             ["Mutual Information", mutual_info_classif]]) #, index=[0, 1])

# array of num_features to compare
#  12 max
# more than that and the funciton breaks, as it tries to inlcude all the zero importance functions
# which is longer than the size of the df that is initialised to store the data
# so it throws an error
num_features_arr = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# target attributes - exclude from training data
target_attrs = ["Risk_infection", "Covid19_positive"]

# split features and target
X = df_covid19.drop(columns=target_attrs)

# dfs to collate data for feature selection comparison
top_feats = pd.DataFrame(columns=['ANOVA', 'Mutual Information', 'n_features', 'target'])
feat_scores = pd.DataFrame(columns=['Attribute', 'ANOVA', 'Mutual Information', 'n_features', 'target'])
model_accuracy_performance = pd.DataFrame(columns=['accuracy', 'dataset', 'selector','classifier', 'n_features', 'target'])

# loop over the target attributes
for i in range(len(target_attrs)):
    # set the labels to the current target attribute 
    y = df_covid19[target_attrs[i]]
    # for each target attribute, compare [x] features 
    for j in range(len(num_features_arr)):
        # execute function to get results for current combination of target_attr and num_features
        curr_feats, curr_scores, curr_accuracies = compare_feat_selectors(X, y, num_features_arr[j],
                                                                          score_functions, package_functions)
        # add current target:n_features for analysis & plotting
        for df in [curr_feats, curr_scores, curr_accuracies]:
            df['target'] = y.name
            df['n_features'] = num_features_arr[j]
        
        # store results
        top_feats = pd.concat([curr_feats, top_feats], ignore_index=True)
        feat_scores = pd.concat([curr_scores, feat_scores], ignore_index=True)
        model_accuracy_performance = pd.concat([model_accuracy_performance, curr_accuracies], ignore_index=True)

# display feature scores for each target
print("Covid19_positive Feat Scores")
pos_scores = feat_scores.loc[
    (feat_scores["n_features"] == num_features_arr[-1]) &
    (feat_scores["target"] == "Covid19_positive")
].drop(['n_features', 'target'], axis=1).sort_values(by="ANOVA", ascending=False).reset_index(drop=True)
# uncomment to export feature scores for covid19_positive to csv
# pos_scores.to_csv("./covid19_positive_feature_scores.csv", index=False)

print("Risk_infection Feat Scores")
infctn_scores = feat_scores.loc[
    (feat_scores["n_features"] == num_features_arr[-1]) &
    (feat_scores["target"] == "Risk_infection")
].drop(['n_features', 'target'], axis=1).sort_values(by="ANOVA", ascending=False).reset_index(drop=True)
# uncomment to export feature scores for risk_infection to csv
# infctn_scores.to_csv("./risk_infection_feature_scores.csv", index=False)

# plot training and test accuracies for each target:feat_selector:classifier:n_features
comp_plt = sns.relplot(
    data=model_accuracy_performance, kind="line",
    x="n_features", y="accuracy", hue="dataset",
    style="classifier", row="target", col="selector",
    markers=True
)

value_tick = range( num_features_arr[0], num_features_arr[-1]+1, 1)

for ax in comp_plt.axes.flat:
    labels = ax.get_xticklabels() # get x labels
    ax.set_xticks(ticks=value_tick) # set new labels

sns.move_legend(comp_plt, loc='lower right', 
                ncols=2, bbox_to_anchor=(0.3, 0.1, 0.5, 0.5))

# construct df for covid19_positive (feat_selector=ANOVA) plot
positive_df = model_accuracy_performance.loc[
    model_accuracy_performance['target'] == "Covid19_positive"
].drop("target", axis=1).reset_index(drop=True)

# plot 
pos_plt = sns.relplot(
    data=positive_df.loc[positive_df['selector'] == "ANOVA"],
    kind="line", x="n_features", y="accuracy", hue="dataset",
    col="classifier", markers=True, estimator=None
)
value_tick = range( num_features_arr[0], num_features_arr[-1]+1, 1)
for ax in pos_plt.axes.flat:
    labels = ax.get_xticklabels() # get x labels
    ax.set_xticks(ticks=value_tick) # set new labels
    ax.set_ylabel("Accuracy")
    ax.set_xlabel(None)
sns.move_legend(pos_plt, title=None, loc="upper right", bbox_to_anchor=(0.9, 0.9))
plt.suptitle('Accuracy of Classification Models Predicting Covid19 Positive', y = 1.03)
pos_plt.fig.text(0.35, 0.0, "Number of Features Selected with ANOVA")

# construct df for infection_risk (feat_selector=ANOVA) plot
infection_df = model_accuracy_performance.loc[
    model_accuracy_performance['target'] == "Risk_infection"].drop("target", axis=1)
infct_plt = sns.relplot(
    data=infection_df.loc[infection_df['selector'] == "ANOVA"],
    kind="line", x="n_features", y="accuracy", hue="dataset",
    col="classifier", markers=True, estimator=None
)
value_tick = range( num_features_arr[0], num_features_arr[-1]+1, 1)
for ax in infct_plt.axes.flat:
    labels = ax.get_xticklabels() # get x labels
    ax.set_xticks(ticks=value_tick) # set new labels
    ax.set_ylabel("Accuracy")
    ax.set_xlabel(None)
sns.move_legend(infct_plt, title=None, loc="upper right", bbox_to_anchor=(0.9, 0.9))
plt.suptitle('Accuracy of Classification Models Predicting Infection Risk', y = 1.03)
infct_plt.fig.text(0.35, 0.0, "Number of Features Selected with ANOVA")
