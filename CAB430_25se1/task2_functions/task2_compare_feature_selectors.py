# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import accuracy_score, classification_report

def compare_feat_selectors(X, y, num_features, feat_select_score_funcs, packages_arr,
                           classifier_names=["Decision Tree Classifier", "Gaussian Naive Bayes"], rs=42):
  # packages_arr = [pd, np, SelectKBest, train_test_split, DecisionTreeClassifier, GaussianNB]
  pd = packages_arr[0]
  np = packages_arr[1]
  SelectKBest = packages_arr[2]
  train_test_split = packages_arr[3]
  DecisionTreeClassifier = packages_arr[4]
  GaussianNB = packages_arr[5]
  
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
  model_accuracies = pd.DataFrame(columns=['accuracy', 'dataset', 'classifier'])
  
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
                                'dataset':["training", "test"], 'classifier':[classifier_names[0], classifier_names[0]]})
    model_accuracies = pd.concat([model_accuracies, dt_accuracy], ignore_index=True)
    
    # Train the GNB
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    gnb_accuracy = pd.DataFrame({'accuracy':[gnb.score(X_train, y_train), gnb.score(X_test, y_test)],
                                 'dataset':["training", "test"], 'classifier':[classifier_names[1], classifier_names[1]]})
    model_accuracies = pd.concat([model_accuracies, gnb_accuracy], ignore_index=True)
  
  scores_df.reset_index(inplace=True)
  scores_df.rename({'index':'Attribute'}, axis=1, inplace=True)
  
  return top_sel_feats, scores_df, model_accuracies
