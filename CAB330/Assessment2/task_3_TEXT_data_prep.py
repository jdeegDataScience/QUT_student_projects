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

def preprocess_movie_data(raw_movie_data, optimise=False):
    # drop all cols except 'Description'
    preprocess_df = raw_movie_data.loc[:, ['Description']]
    
    # if default analysis
    if optimise==False:
        stopwords = set(sw.words('english'))
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2))
    else: # add additional stop words and strip noisy phrases from data
        stopwords = set(sw.words('english')).union(set(('c', 'r', 'u', 'film')))
        preprocess_df['Description'] = preprocess_df['Description'].str.split('\. --',expand=True).iloc[:,0]
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2), min_df=0.05, max_df=0.7)
    
    X = tfidf_vec.fit_transform(preprocess_df.Description)
    
    return tfidf_vec, X
