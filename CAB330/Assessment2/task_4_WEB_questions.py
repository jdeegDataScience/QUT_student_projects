import pandas as pd
import numpy as np
from collections import defaultdict
import datetime
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings("ignore")

# Load the CSV file into a DataFrame
web_data = pd.read_csv('Weblog_v1.csv')

# Task 1 & 2 - Load data and preprocess, extract variables for cluster analysis 
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

# Call the preprocess_web_data function with the DataFrame
web_df = preprocess_web_data(df)

# Task 3 - Apply clustering analysis - find optimal K
-----------------------

# list to save the clusters and cost
clusters = []
inertia_vals = []
explore_range = range(2,15,2)

for k in explore_range:
    # train clustering with the specified K
    model = KMeans(n_clusters=k, random_state=rs)
    model.fit(X)
    
    # append model to cluster list
    clusters.append(model)
    inertia_vals.append(model.inertia_)

# plot the inertia vs K values
plt.plot(explore_range, inertia_vals, marker='*')
plt.show()

# Define a range of cluster numbers to test
cluster_range = range(2, 9)  # Test clusters from 2 to 8

# Iterate over different cluster numbers
for num_clusters in cluster_range:
    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    y = kmeans.fit_predict(X)

    # Compute silhouette score
    silhouette_avg = silhouette_score(X, y)
    print(f"Number of Clusters: {num_clusters}, Silhouette Score: {silhouette_avg}")

    # Sum of intra-cluster distances
    print(f"Number of Clusters: {num_clusters}, Sum of intra-cluster distance: {kmeans.inertia_}")

    print("\n")  


# Apply k-means clustering and plot
num_clusters = 4
rs=42
kmeans = KMeans(n_clusters=num_clusters, random_state=rs)
kmeans.fit(X)
y = kmeans.predict(X)
processed_df['cluster'] = y

# how many records are in each cluster
print("Cluster membership")
print(processed_df['cluster'].value_counts())

# sum of intra-cluster distances
print("Sum of intra-cluster distance:", kmeans.inertia_)

cluster_g = sns.pairplot(processed_df, hue='cluster')
plt.show()
