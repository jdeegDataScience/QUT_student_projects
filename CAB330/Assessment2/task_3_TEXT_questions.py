# import packages
import string
import pandas as pd

# natural language toolkit
from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

# scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

# maths
from scipy.spatial.distance import euclidean
from math import sqrt

# load dataset
# M_metadata_v1.csv
movie_data = pd.read_csv('M_metadata_v1.csv', na_filter=False)

# initialise resources and constants
rs = 21
lemmatizer = WordNetLemmatizer()
punct = set(string.punctuation)
# stopwords are not initialised here as different sets are used throughout the analysis

# initialise functions for task
# function to visualise text cluster
def visualise_text_cluster(n_clusters, cluster_centers, terms, num_word = 10):
    # -- Params --
    # cluster_centers: cluster centers of fitted/trained KMeans/other centroid-based clustering
    # terms: terms used for clustering
    # num_word: number of terms to show per cluster. Change as you please.
    
    # find features/terms closest to centroids
    ordered_centroids = cluster_centers.argsort()[:, ::-1]
    
    for cluster in range(n_clusters):
        print("Top terms for cluster {}:".format(cluster), end=" ")
        for term_idx in ordered_centroids[cluster, :num_word]:
            print(terms[term_idx], end=', ')
        print()

# creates tf-idf terms; a bit slow, run only occasionaly
# Param - document_col: collection of raw document text that you want to analyse
def calculate_tf_idf_terms(document_col):
    # use count vectorizer to find TF and DF of each term
    count_vec = CountVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2))
    X_count = count_vec.fit_transform(document_col)
    
    # create list of terms and their tf and df
    terms = [{'term': t, 'idx': count_vec.vocabulary_[t],
              'tf': X_count[:, count_vec.vocabulary_[t]].sum(),
              'df': X_count[:, count_vec.vocabulary_[t]].count_nonzero()}
             for t in count_vec.vocabulary_]
    
    return terms

# visualisation of ZIPF law
# --- Param ---
    # terms: collection of terms dictionary from calculate_tf_idf_terms function
    # itr_step: used to control how many terms that you want to plot.
    #           Num of terms to plot = N terms / itr_step
def visualise_zipf(terms, itr_step = 50):
    # sort terms by its frequency
    terms.sort(key=lambda x: (x['tf'], x['df']), reverse=True)
    
    # select a few of the terms for plotting purpose
    sel_terms = [terms[i] for i in range(0, len(terms), itr_step)]
    labels = [term['term'] for term in sel_terms]
    
    # plot term frequency ranking vs its DF
    plt.plot(range(len(sel_terms)), [x['df'] for x in sel_terms])
    plt.xlabel('Term frequency ranking')
    plt.ylabel('Document frequency')
    
    max_x = len(sel_terms)
    max_y = max([x['df'] for x in sel_terms])
    
    # annotate the points
    prev_x, prev_y = 0, 0
    for label, x, y in zip(labels,range(len(sel_terms)), [x['df'] for x in sel_terms]):
        # calculate the relative distance between labels to increase visibility
        x_dist = (abs(x - prev_x) / float(max_x)) ** 2
        y_dist = (abs(y - prev_y) / float(max_y)) ** 2
        scaled_dist = sqrt(x_dist + y_dist)
        
        if (scaled_dist > 0.1):
            plt.text(x+2, y+2, label, {'ha': 'left', 'va': 'bottom'}, rotation=30)
            prev_x, prev_y = x, y
    
    plt.show()


# ---

# 3.2
# no stopwords required for default ZIPF plot
stopwords = ''
# slow, run infrequently
terms = calculate_tf_idf_terms(movie_data.Description)
visualise_zipf(terms)

# ---

# 3.3
# additional terms identified during analysis that are...
# not useful for clustering and...
# that are not contained in the preset stop words list
movie_stop = set(('c', 'r', 'u', 'film'))
print(movie_stop)

# ---

# 3.4
# tf idf vectoriser
tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2))
X = tfidf_vec.fit_transform(movie_data.Description)

# number of input features
print(len(tfidf_vec.get_feature_names_out()))

# ---

# 3.5 Optimal K
# apply SVD/LSA transformation 
svd = TruncatedSVD(n_components=100, random_state=rs)
X_trans = svd.fit_transform(X_filter)

# list to save the clusters and cost
clusters = []
inertia_vals = []
explore_range = range(17, 22, 1)

for k in explore_range:
    # train clustering with the specified K
    model = KMeans(n_clusters=k, random_state=rs)
    model.fit(X_trans)
    
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
    value = silhouette_score(X_trans, clusters[clust].predict(X_trans))
    cluster_silhouettes[key] = value
    
#    print(clusters[clust])
#    print(f"Silhouette score for k={key}", value)
#    print()

max_sil_score = max(cluster_silhouettes.values())
max_sil_clusters = get_key_by_value(cluster_silhouettes, max_sil_score)
print("Number of clusters: ", max_sil_score, "\nSilhouette Score: ", max_sil_clusters)

# ---

# 3.6 - Describe Clusters and Display results
# number of clusters
print("Number of clusters: ", max_sil_clusters, "\nSilhouette Score: ", max_sil_score)

# K-means clustering using LSA-transformed X
svd_kmeans = KMeans(n_clusters=max_sil_clusters, random_state=rs).fit(X_trans)

# transform cluster centers back to original feature space for visualisation
original_space_centroids = svd.inverse_transform(svd_kmeans.cluster_centers_)

# visualisation
visualise_text_cluster(svd_kmeans.n_clusters, original_space_centroids, tfidf_filter.get_feature_names_out(), num_word = 15)
