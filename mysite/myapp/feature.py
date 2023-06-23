import os
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
from scipy.sparse import hstack
from sklearn.metrics import confusion_matrix
import numpy as np
import gensim
from sklearn.metrics import classification_report
# from django.conf import settings

# DATASET_PATH = str(settings.BASE_DIR+'../dataset/')


def RecallPrecisionFScore(y_test, y_pred):
    report = classification_report(y_test, y_pred)
    print("report: ", report)

    arr = confusion_matrix(y_test, y_pred)

    fp = arr[0][1] + arr[0][2] + arr[1][0] + arr[1][2] + arr[2][1] + arr[2][2]
    fn = arr[1][0] + arr[2][0] + arr[0][1] + arr[2][1] + arr[0][2] + arr[1][2]

    tp = arr[0][0] + arr[1][1] + arr[2][2]
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2 * precision * recall) / (precision + recall)

    print("Precision: ", float('{0:.2f}'.format(precision * 100)))
    print("Recall: ", float('{0:.2f}'.format(recall * 100)))
    print("F1 score: ", float('{0:.2f}'.format(f1 * 100)))

    return float('{0:.2f}'.format(precision * 100)), float('{0:.2f}'.format(recall * 100)), float(
        '{0:.2f}'.format(f1 * 100))


class Word2VecVectorizer:
    def __init__(self, model):
        print("Loading in word vectors...")
        self.word_vectors = model
        print("Finished loading in word vectors")

    def fit(self, data):
        pass

    def transform(self, data):

        # determine the dimensionality of vectors
        v = self.word_vectors.get_vector('I')
        self.D = v.shape[0]

        X = np.zeros((len(data), self.D))
        n = 0
        emptycount = 0
        for sentence in data:
            tokens = sentence.split()
            vecs = []
            m = 0
            for word in tokens:
                try:
                    # throws KeyError if word not found
                    vec = self.word_vectors.get_vector(word)
                    vecs.append(vec)
                    m += 1
                except KeyError:
                    pass
            if len(vecs) > 0:
                vecs = np.array(vecs)
                X[n] = vecs.mean(axis=0)
            else:
                emptycount += 1
            n += 1
        print("Numer of samples with no words found: %s / %s" % (emptycount, len(data)))
        return X

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)


def embedding_feature_based_combination(df_train, df_test, c, ux, uy, cx, cy):
    path_parent = os.path.dirname(os.getcwd())
    # os.chdir( path_parent )
    ft = gensim.models.KeyedVectors.load_word2vec_format("../embeddings/cc.en.300.vec")

    X_train = df_train["text"]
    X_test = df_test["text"]

    y_train = df_train["label"]
    y_test = df_test["label"]

    vectorizer = Word2VecVectorizer(ft)
    Xtrain = vectorizer.fit_transform(X_train)

    Xtest = vectorizer.transform(X_test)

    # word
    tfidf_vect_ngram_word = TfidfVectorizer(analyzer='word', ngram_range=(ux, uy))
    tfidf_vect_ngram_word.fit(X_train)
    xtrain_word = tfidf_vect_ngram_word.transform(X_train)
    xtest_word = tfidf_vect_ngram_word.transform(X_test)

    # char
    tfidf_vect_ngram_char = TfidfVectorizer(analyzer='char', ngram_range=(cx, cy))
    tfidf_vect_ngram_char.fit(X_train)
    xtrain_char = tfidf_vect_ngram_char.transform(X_train)
    xtest_char = tfidf_vect_ngram_char.transform(X_test)

    tfidf_matrix_word_char_train = hstack((xtrain_word, xtrain_char, Xtrain))
    tfidf_matrix_word_char_test = hstack((xtest_word, xtest_char, Xtest))

    linear = LinearSVC(C=c, penalty='l2', loss='squared_hinge')

    linear.fit(tfidf_matrix_word_char_train, y_train)

    pred = linear.predict(tfidf_matrix_word_char_test)

    precision, recall, f1 = RecallPrecisionFScore(y_test, pred)


def embedding_feature(df_train, df_test, c):
    path_parent = os.path.dirname(os.getcwd())
    # os.chdir( path_parent )

    ft = gensim.models.KeyedVectors.load_word2vec_format("../embeddings/cc.en.300.vec")

    X_train = df_train["text"]
    X_test = df_test["text"]

    y_train = df_train["label"]
    y_test = df_test["label"]

    vectorizer = Word2VecVectorizer(ft)
    Xtrain = vectorizer.fit_transform(X_train)

    Xtest = vectorizer.transform(X_test)

    linear = LinearSVC(C=c, penalty='l2', loss='squared_hinge')

    linear.fit(Xtrain, y_train)

    pred = linear.predict(Xtest)
    print(pred)

    precision, recall, f1 = RecallPrecisionFScore(y_test, pred)


def feature_based_combination(df_train, df_test, c, ux, uy, cx, cy):
    X_train = df_train["text"]
    X_test = df_test["text"]

    y_train = df_train["label"]
    y_test = df_test["label"]

    # word
    tfidf_vect_ngram_word = TfidfVectorizer(analyzer='word', ngram_range=(ux, uy))
    tfidf_vect_ngram_word.fit(X_train)
    xtrain_word = tfidf_vect_ngram_word.transform(X_train)
    xtest_word = tfidf_vect_ngram_word.transform(X_test)

    # char
    tfidf_vect_ngram_char = TfidfVectorizer(analyzer='char', ngram_range=(cx, cy))
    tfidf_vect_ngram_char.fit(X_train)
    xtrain_char = tfidf_vect_ngram_char.transform(X_train)
    xtest_char = tfidf_vect_ngram_char.transform(X_test)

    tfidf_matrix_word_char_train = hstack((xtrain_word, xtrain_char))
    tfidf_matrix_word_char_test = hstack((xtest_word, xtest_char))

    linear = LinearSVC(C=c, penalty='l2', loss='squared_hinge')

    linear.fit(tfidf_matrix_word_char_train, y_train)

    pred = linear.predict(tfidf_matrix_word_char_test)

    precision, recall, f1 = RecallPrecisionFScore(y_test, pred)


def feature_based(df_train, df_test, c, x1, y1, gram):
    X_train = df_train["text"]
    X_test = df_test["text"]

    y_train = df_train["label"]
    y_test = df_test["label"]

    tfidf_vect_ngram = TfidfVectorizer(analyzer=gram, ngram_range=(x1, y1), tokenizer=lambda x: x.split())
    tfidf_vect_ngram.fit(X_train)
    feature_names = tfidf_vect_ngram.get_feature_names_out()
    xtrain = tfidf_vect_ngram.transform(X_train)
    xtest = tfidf_vect_ngram.transform(X_test)

    linear = LinearSVC(C=c, penalty='l2', loss='squared_hinge')
    linear.fit(xtrain, y_train)

    pred = linear.predict(xtest)

    precision, recall, f1 = RecallPrecisionFScore(y_test, pred)


if __name__ == '__main__':
    path_parent = os.path.dirname(os.getcwd())
    print(path_parent)
    # os.chdir(path_parent)
    # DATASET_PATH = '..\\dataset\\'

    df_train = pd.read_csv("../data/train_df.csv")
    df_val = pd.read_csv("../data/val_df.csv")
    df_test = pd.read_csv("../data/test_df.csv")

    model_name = input("Please Specify the Model Name: ")

    if model_name == "Unigram":
        feature_based(df_train, df_test, c=1, x1=1, y1=1, gram="word")

    elif model_name == "Bigram":
        feature_based(df_train, df_test, c=10, x1=2, y1=2, gram="word")

    elif model_name == "Trigram":
        feature_based(df_train, df_test, c=1, x1=3, y1=3, gram="word")

    elif model_name == "U+B":
        feature_based(df_train, df_test, c=1, x1=1, y1=2, gram="word")

    elif model_name == "B+T":
        feature_based(df_train, df_test, c=10, x1=2, y1=3, gram="word")

    elif model_name == "U+B+T":
        feature_based(df_train, df_test, c=10, x1=1, y1=3, gram="word")

    elif model_name == "Char 2-gram":
        feature_based(df_train, df_test, c=1, x1=2, y1=2, gram="char")

    elif model_name == "Char 3-gram":
        feature_based(df_train, df_test, c=1, x1=3, y1=3, gram="char")

    elif model_name == "Char 4-gram":
        feature_based(df_train, df_test, c=1, x1=4, y1=4, gram="char")

    elif model_name == "Char 5-gram":
        feature_based(df_train, df_test, c=1, x1=5, y1=5, gram="char")

    elif model_name == "C2+C3":
        feature_based(df_train, df_test, c=1, x1=2, y1=3, gram="char")

    elif model_name == "C3+C4":
        feature_based(df_train, df_test, c=1, x1=3, y1=4, gram="char")

    elif model_name == "C4+C5":
        feature_based(df_train, df_test, c=1, x1=4, y1=5, gram="char")

    elif model_name == "C2+C3+C4":
        feature_based(df_train, df_test, c=1, x1=2, y1=4, gram="char")

    elif model_name == "C3+C4+C5":
        feature_based(df_train, df_test, c=1, x1=3, y1=5, gram="char")

    elif model_name == "C2+C3+C4+C5":
        feature_based(df_train, df_test, c=1, x1=2, y1=5, gram="char")

    elif model_name == "U+B+C3+C4+C5":
        feature_based_combination(df_train, df_test, c=1, ux=1, uy=2, cx=3, cy=5)

    elif model_name == "U+B+C2+C3+C4+C5":
        feature_based_combination(df_train, df_test, c=1, ux=1, uy=2, cx=2, cy=5)

    elif model_name == "U+B+T+C2+C3+C4+C5":
        feature_based_combination(df_train, df_test, c=1, ux=1, uy=3, cx=2, cy=5)

    elif model_name == "Embeddings":
        embedding_feature(df_train, df_test, c=10)

    elif model_name == "U+B+C2+C3+C4+C5+E":
        embedding_feature_based_combination(df_train, df_test, c=1, ux=1, uy=2, cx=2, cy=5)

    elif model_name == "U+B+T+C2+C3+C4+C5+E":
        embedding_feature_based_combination(df_train, df_test, c=1, ux=1, uy=3, cx=2, cy=5)