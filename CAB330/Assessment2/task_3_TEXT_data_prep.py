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
    
    # explicit stopword variables
    engStop = sw.words('english')
    
    movieStop = set(('c', 'r', 'u', 'film', 'films',
                     'life', 'love', 'one', 'story', 'lives', 'living',
                     'director', 'direct', 'directs', 'directing',
                     'feature', 'features', 'featuring',
                     'star', 'stars', 'starring',
                     'world', 'rovi', 'award', 'academy',
                     'year', 'years', 'two', 
                     'find', 'finds', 'power', 'powers', 'powerful',
                     'include', 'includes', 'including',
                     'also', 'first', 'filmmaker', 'movie', 'movies',
                     'dream', 'would', 'use'))
    
    # split the document into sentences
    for sent in sent_tokenize(document):
        # split the document into tokens and then create part of speech tag for each token
        for token, tag in pos_tag(wordpunct_tokenize(sent)):
            # preprocess and remove unnecessary characters
            token = token.lower()
            token = token.strip()
            token = token.strip('_')
            token = token.strip('*')
            
            isEngStop = token in engStop
            
            isMovieStop = token in movieStop
            
            isPunct = all(char in punct for char in token)
            

            # If not stopword or punctuation
            if not isEngStop and not isMovieStop and not isPunct:
                # Lemmatize the token and add back to the tokens list
                lemma = lemmatize(token, tag)
                tokens.append(lemma)

    return tokens

def cab_tokenizer_no_stop(document):    
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
            
            # if token is just punctuation
            isPunct = all(char in punct for char in token)
            

            # If not punctuation
            if not isPunct:
                # Lemmatize the token and add back to the tokens list
                lemma = lemmatize(token, tag)
                tokens.append(lemma)

    return tokens

def preprocess_movie_data(raw_movie_data, optimise=False):
    # drop all cols except 'Description'
    preprocess_df = raw_movie_data.loc[:, ['Description']]
    
    if optimise: # strip noisy phrases from data and filter terms
        preprocess_df['Description'] = preprocess_df['Description'].str.split(r'\. --',expand=True).iloc[:,0]
        preprocess_df['Description'] = preprocess_df['Description'].str.split(r'\. ~',expand=True).iloc[:,0]
        preprocess_df['Description'] = preprocess_df['Description'].str.split(r'\. \([cC]\)',expand=True).iloc[:,0]
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer, ngram_range=(1,2), min_df=0.06, max_df=0.3)
    
    # otherwise, default analysis
    else: # default vectorizer with unigram and bigram tokens
        tfidf_vec = TfidfVectorizer(tokenizer=cab_tokenizer_no_stop, ngram_range=(1,2))
        print("Filter stopwords: ", optimise)
    
    X = tfidf_vec.fit_transform(preprocess_df.Description)
    
    return tfidf_vec, X
    X = tfidf_vec.fit_transform(preprocess_df.Description)
    
    return tfidf_vec, X
