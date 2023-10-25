import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import distance

# random state
rs = 21

# load dataset
music_data = pd.read_csv('Music_shop_v1.csv', na_filter=False, encoding='latin-1')

# ---

# 1.1 - Clean dataset ; desription of steps in README doc
# preprocess data 
music_df = preprocess_music_data(music_data)

# ---

# 1.2 - Variables included n analysis
music_df.columns

# ---

# 1.3 - Default clustering Model
# convert df values to matrix
X = music_df.values
default_cluster = KMeans(n_clusters=3, random_state=rs).fit(X)

# 1.3.a - Default Model Cluster Membership
# assign cluster ID to each record in X
default_y = default_cluster.predict(X)
music_df['Default_Cluster_ID'] = default_y

# how many records are in each cluster
print("Default Model Cluster Membership")
print(music_df['Default_Cluster_ID'].value_counts())

# 1.3.b - Default Model Cluster Distributions
# pairplot the cluster distribution
cluster_default = sns.pairplot(music_df, hue='Default_Cluster_ID')
plt.show()


# drop unnecessary col to avoid interferring with future analyses
music_df.drop(columns='Default_Cluster_ID', inplace=True)

# ---

# 1.4 - Effects of Feature Standardization: does it result in a better model?
# scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

scaled_cluster = KMeans(n_clusters=3, random_state=rs).fit(X_scaled)

# assign cluster ID to each record in X
y_scaled = scaled_cluster.predict(X_scaled)
music_df['Scaled_Cluster_ID'] = y_scaled

# how many records are in each cluster
print("Scaled Cluster Membership")
print(music_df['Scaled_Cluster_ID'].value_counts())

# pairplot scaled cluster distribution
cluster_scaled = sns.pairplot(music_df, hue='Scaled_Cluster_ID')
plt.show()
# drop unnecessary columns
music_df.drop(columns='Scaled_Cluster_ID', inplace=True)bb

# silhouette scores and clustering error for each model
# note the significant drop in 
print("Default model - silhouette score: ", silhouette_score(X, default_cluster.predict(X)))
print("Default model - clustering error: ", default_cluster.inertia_)
print()
print("Scaled model - silhouette score: ", silhouette_score(X_scaled, scaled_cluster.predict(X_scaled)))
print("Scaled model - clustering error: ", scaled_cluster.inertia_)

# ---

## 1.6 - Euclidean Distances between cluster centers based on the optimal K
# list to save the clusters and cost
clusters = []
inertia_vals = []

explore_range = range(4, 6, 1)

for k in explore_range:
    # train clustering with the specified K
    model = KMeans(n_clusters=k, random_state=rs)
    model.fit(X_scaled)
    
    # append model to cluster list
    clusters.append(model)
    inertia_vals.append(model.inertia_)

# plot the inertia vs K values
plt.plot(explore_range, inertia_vals, marker='*')
plt.show()

# programmatically generate and store silhouette scores for later
cluster_silhouettes = {}

for clust in range(len(clusters)):
    key = clusters[clust].n_clusters
    value = silhouette_score(X_scaled, clusters[clust].predict(X_scaled))
    cluster_silhouettes[key] = value
    
    print(clusters[clust])
    print(f"Silhouette score for k={key}", value)
    print()

max_sil_score = max(cluster_silhouettes.values())
max_sil_clusters = get_key_by_value(cluster_silhouettes, max_sil_score)

# generate model to calculate cluster distances
opti_scaled_cluster = KMeans(n_clusters=max_sil_clusters, random_state=rs).fit(X_scaled)

# Initialize a dictionary to store distances
distances = {}

# Iterate through each point
for i, point1 in enumerate(opti_scaled_cluster.cluster_centers_):
    for j, point2 in enumerate(opti_scaled_cluster.cluster_centers_):
        if i != j:  # Ensure you don't calculate the distance from a point to itself
            this_distance = distance.euclidean(point1, point2)
            distances[(i, j)] = this_distance

min_dist = min(distances.values())
max_dist = max(distances.values())
avg_dist = sum(distances.values()) / len(distances)


print(f'The minimum distance between cluster centres is {min_dist:.3} units.')
print(f'The maximum distance between cluster centres is {max_dist:.3} units.')
print(f'The average distance between cluster centres is {avg_dist:.3} units.')

# code block
print(f'We found that K={max_sil_clusters} was optimal, with a silhouette score of {max_sil_score:.3}.')

# ---

# 1.5 - Interpret Cluster Results
# assign cluster ID to each record in X_scaled
y_opti_scaled = opti_scaled_cluster.predict(X_scaled)
music_df['Opti_Scaled_Cluster_ID'] = y_opti_scaled

# how many records are in each cluster
print("Optimum Scaled Cluster Membership")
print(music_df['Opti_Scaled_Cluster_ID'].value_counts())

# prepare the column and bin size
cols = ['Energy', 'Loudness', 'Speechiness', 'Instrumentalness']
n_bins = 20

# pairplot the cluster distribution
cluster_opti_scaled = sns.pairplot(music_df, hue='Opti_Scaled_Cluster_ID')
plt.show()
# only uncomment if not running subsequent codeblocks for Q1.5
# music_df.drop(columns='Opti_Scaled_Cluster_ID', inplace=True)

# inspecting all clusters
clusters_to_inspect = range(max_sil_clusters)

for cluster in clusters_to_inspect:
    # inspecting cluster [x]
    print("Distribution for cluster {}".format(cluster))

    # create subplots
    fig, ax = plt.subplots(nrows=len(cols))
    ax[0].set_title("Cluster {}".format(cluster))

    for j, col in enumerate(cols):
        # create the bins
        bins = np.linspace(min(music_df[col]), max(music_df[col]), 20)
        # plot distribution of the cluster using histogram
        sns.distplot(music_df[music_df['Opti_Scaled_Cluster_ID'] == cluster][col], bins=bins, ax=ax[j], norm_hist=True)
        # plot the normal distribution with a black line
        sns.distplot(music_df[col], bins=bins, ax=ax[j], hist=False, color="k")

    plt.tight_layout()
    plt.show()
