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

# Initialize stopwords here and more
# initialise resources
lemmatizer = WordNetLemmatizer()
punct = set(string.punctuation)
stopwords = set(sw.words('english')).union(set(('c', 'r', 'u', 'film')))
stopwords = set(sw.words('english'))
rs = 21

def lemmatize(token, tag):
    tag = {
        'N': wn.NOUN,
        'V': wn.VERB,
        'R': wn.ADV,
        'J': wn.ADJ
    }.get(tag[0], wn.NOUN)
    return lemmatizer.lemmatize(token, tag)

def cab_tokenizer(document):
    # initialize token list
    tokens = []
    
    # split the document into sentences
    for sent in sent_tokenize(document):
        # split the document into tokens and then create part of speech tag for each token
        for token, tag in pos_tag(wordpunct_tokenize(sent)):
            # preprocess and remove unnecessary characters
            token = token.lower()
            token = token.strip()
            token = token.strip('_')
            token = token.strip('*')

            # If stopword, ignore token and continue
            if token in stopwords:
                continue

            # If punctuation, ignore token and continue
            if all(char in punct for char in token):
                continue

            # Lemmatize the token and add back to the tokens list
            lemma = lemmatize(token, tag)
            tokens.append(lemma)
    
    return tokens

import seaborn as sns
import matplotlib.pyplot as plt

# function to visualise text cluster
def visualise_text_cluster(n_clusters, cluster_centers, terms, num_word = 5):
    # -- Params --
    # cluster_centers: cluster centers of fitted/trained KMeans/other centroid-based clustering
    # terms: terms used for clustering
    # num_word: number of terms to show per cluster. Change as you please.
    
    # find features/terms closest to centroids
    ordered_centroids = cluster_centers.argsort()[:, ::-1]
    
    for cluster in range(n_clusters):
        print("Top terms for cluster {}:".format(cluster), end=" ")
        for term_idx in ordered_centroids[cluster, :5]:
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
  
def preprocess_movie_data(raw_movie_data, optimise=True):
    # drop all cols except 'Description'
    preprocess_df = raw_movie_data.loc[:, ['Description']]
    
    # if default analysis
    if optimise==True:
        stopwords = set(sw.words('english'))
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2))
    else: # add additional stop words and strip noisy phrases from data
        stopwords = set(sw.words('english')).union(set(('c', 'r', 'u', 'film')))
        preprocess_df['Description'] = preprocess_df['Description'].str.split('\. --',expand=True).iloc[:,0]
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2), min_df=0.05, max_df=0.7)
    
    X = tfidf_vec.fit_transform(preprocess_df.Description)
    
    return tfidf_vec, X
  
# Task 3.4
# tf idf vectoriser
tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2))
X = tfidf_vec.fit_transform(movie_data.Description)

# number of input features
print(len(tfidf_vec.get_feature_names_out()))

# Task 3.6 ?
# K means clustering using the term vector
kmeans = KMeans(n_clusters=10, random_state=rs).fit(X)

# call it
visualise_text_cluster(kmeans.n_clusters, kmeans.cluster_centers_, tfidf_vec.get_feature_names_out())

# Task 3.2
terms = calculate_tf_idf_terms(movie_data.Description)
visualise_zipf(terms)

# Task 3.4 - trying another tf idf vectoriser, to compare
# tf idf vectoriser
filter_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2),
                            min_df=2, max_df=0.8)
X_filter = filter_vec.fit_transform(movie_data.Description)

# number of input features
print(len(filter_vec.get_feature_names_out()))

# K means clustering using the new term vector, time it for comparison to SVD
kmeans_fil = KMeans(n_clusters=10, random_state=rs).fit(X_filter)

# visualisation
visualise_text_cluster(kmeans_fil.n_clusters, kmeans_fil.cluster_centers_, 
                       filter_vec.get_feature_names_out())

# K-means clustering - SVD
svd = TruncatedSVD(n_components=100, random_state=42)
X_trans = svd.fit_transform(X_filter)

# sort the components by largest weighted word
sorted_comp = svd.components_.argsort()[:, ::-1]
terms = filter_vec.get_feature_names_out()

# visualise word - concept/component relationships
for comp_num in range(10):
    print("Top terms in component #{}".format(comp_num), end=" ")
    for i in sorted_comp[comp_num, :5]:
        print(terms[i], end=", ")
    print()

# K-means clustering using LSA-transformed X
svd_kmeans = KMeans(n_clusters=10, random_state=rs).fit(X_trans)

# transform cluster centers back to original feature space for visualisation
original_space_centroids = svd.inverse_transform(svd_kmeans.cluster_centers_)

# visualisation
visualise_text_cluster(svd_kmeans.n_clusters, original_space_centroids, filter_vec.get_feature_names_out())

# Task 3.5 - finding optimal K - using the elbow method
#list to save the clusters 
clusters = []
inertia_vals = []

# this whole process should take a while
for k in range(2, 15, 2):
    # train clustering with the specified K
    model = KMeans(n_clusters=k, random_state=rs)
    model.fit(X)
    
    # append model to cluster list
    clusters.append(model)
    inertia_vals.append(model.inertia_)
    
# plot the inertia vs K values
plt.plot(range(2,15,2), inertia_vals, marker='*')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()
