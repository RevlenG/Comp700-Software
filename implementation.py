#Packages and Libraries
import pandas as pd
import numpy as np
import re
import nltk
import math
import matplotlib.pyplot as plt
import spacy
from nltk.corpus import stopwords
from gensim import corpora, models
from sklearn import metrics
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import ward, linkage, fcluster

nltk.download('stopwords')
nltk.download('wordnet')

##################################################################################################

def preprocessing(file_path, tweet_col_name, sentiment_col_name, company_col_name):
    #Preprocessing
    df = pd.read_csv(file_path)
    df = df[[sentiment_col_name, company_col_name, tweet_col_name]]
    df = df.rename(columns={tweet_col_name: "Tweet", company_col_name:"Company", sentiment_col_name: "Sentiment"})

    #Filtering only the IPhone and IPad reviews
    df = df.loc[df["Company"].isin(["United"])]

    #Removal of columns where the sentiment was neutral
    df = df[df["Sentiment"] != "neutral"]

    #Removal of duplicate tweets
    # sorted_data = df.sort_values('Tweet', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    df.drop_duplicates(subset={"Tweet", "Sentiment"}, keep='first', inplace=True)

    custom_stop_words = ["rt", "link"]
    stop_words = stopwords.words('english') + custom_stop_words

    #Lowercasing text and removal of puncuation, stop words, html tags
    def preprocess(text, stemmer, lemmatizer):
        text = re.sub("@\S+|https?:\S+|http?:\S|[^@A-Za-z]+", ' ', str(text).lower()).strip()
        tokens = []
        stem_tokens = []
        lemma_tokens = []
        for token in text.split():
            if token not in stop_words:
                tokens.append(token)
            stem_tokens.append(snow_stemmer.stem(token))

        review = lemmatizer(" ".join(tokens))
        for token in review:
            if token.pos_ in ["NOUN", "ADJ", "VERB", "ADV"]:
                lemma_tokens.append(token.lemma_)
        return [" ".join(tokens), " ".join(stem_tokens), " ".join(lemma_tokens)]

    snow_stemmer = nltk.stem.SnowballStemmer("english")
    lemmatizer = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    df["Cleaned_Tweet"] = df.Tweet.apply(lambda x: preprocess(x, snow_stemmer, lemmatizer))
    df[["Cleaned_Tweet", "Stemmed_Tweet", "Lemmatized_Tweet"]] = pd.DataFrame(df["Cleaned_Tweet"].tolist(), index=df.index)
    df["Tokens"] = df["Cleaned_Tweet"].apply(lambda text: text.split())
    df["Lemmatized_Tokens"] = df["Lemmatized_Tweet"].apply(lambda text: text.split())

    df.reset_index(drop=True, inplace=True)

    pos_df = df[df["Sentiment"] == "positive"]
    pos_df.reset_index(drop=True, inplace=True)
    neg_df = df[df["Sentiment"] == "negative"]
    neg_df.reset_index(drop=True, inplace=True)

    return df, pos_df, neg_df

#######################################################################################################

def vectorization(pos_df, neg_df):
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,3),
                             stop_words="english", min_df=3)
    pos_vectors = vectorizer.fit_transform(pos_df["Lemmatized_Tweet"])
    pos_feature_names = vectorizer.get_feature_names_out()
    neg_vectors = vectorizer.fit_transform(neg_df["Lemmatized_Tweet"])
    neg_feature_names = vectorizer.get_feature_names_out()

    return pos_vectors, neg_vectors, pos_feature_names, neg_feature_names

###########################################################################################################

def k_means_clustering(vector, feature_names, df):
  # Determining the number of clusters
  upper = min(40, math.floor(0.1 * vector.shape[1]))
  max_sil = -999
  num_clusters = 2

  for i in range (2, upper):
    model = KMeans(n_clusters=i, n_init = "auto", random_state=42)
    y_pred = model.fit_predict(vector)
    sil_score = metrics.silhouette_score(vector, y_pred, metric='euclidean')
    if max_sil < sil_score:
      max_sil = sil_score
      num_clusters = i

  model = KMeans(n_clusters=num_clusters, n_init = "auto", random_state=42)
  y_pred = model.fit_predict(vector)
  order_centroids = model.cluster_centers_.argsort()[:, ::-1]

  df['KMeans_Cluster_Labels'] = y_pred
  
  clusters = []
  for i in range(num_clusters):
      cluster = []
      for ind in order_centroids[i, :10]:
          cluster.append(feature_names[ind])
      clusters.append(cluster)

  return clusters, df

################################################################################################

def hierarchical_clustering(vector, feature_names, df):
  # Determining the number of clusters
  upper = min(40, math.floor(0.1 * vector.shape[1]))
  max_sil = -999
  num_clusters = 20

  for i in range (2, upper):
    model = AgglomerativeClustering(n_clusters=i, metric='euclidean', linkage='ward')
    y_pred = model.fit_predict(vector.toarray())
    sil_score = metrics.silhouette_score(vector, y_pred, metric='euclidean')
    if max_sil < sil_score:
      max_sil = sil_score
      num_clusters = i

  model = AgglomerativeClustering(n_clusters=num_clusters, metric='euclidean', linkage='ward')
  y_pred = model.fit_predict(vector.toarray())
  linkage_matrix = linkage(vector.toarray(), method='ward')
  flat_clusters = fcluster(linkage_matrix, t=20, criterion='maxclust')

  df['Agglo_Cluster_Labels'] = y_pred

  clusters = []
  for i in range(num_clusters):
      cluster = []
      for ind in np.argsort(vector.toarray()[i])[::-1][:10]:
          cluster.append(feature_names[ind])
      clusters.append(cluster)

  return clusters, df

################################################################################################

def topic_modelling(clusters):
  output_topics = []
  for cluster in clusters:
    # Create a dictionary with explicit word-to-ID mapping
    dictionary = corpora.Dictionary([cluster])

    # Create a corpus with word IDs
    corpus = [dictionary.doc2bow(token) for token in [cluster]]

    # Create an LDA model
    lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary)

    # Print the topics with words
    topics = lda_model.show_topics(num_topics=1, num_words=2, formatted=True)
    temp = []
    for topic in topics:
        temp = temp + re.findall(r'"([^"]*)"', topic[1])
    output_topics.append(temp)

  return output_topics

################################################################################################