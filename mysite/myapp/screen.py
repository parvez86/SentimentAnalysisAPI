from django.conf import settings
from django.conf import settings
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC
import pandas as pd
import numpy as np

from myapp.Word2VecVectorizer import Word2VecVectorizer
from myapp.util import process_text
import gensim
import os

isFineTuned = False
SENTIMENT_NAMES = ["negative", "neutral", "positive"]
model = None
vectorizer = None


def build_model():
    model_path = "embeddings/cc.en.300.vec"
    data_path = "data/train_df.csv"

    # print("data path: ", data_path)

    # read train data
    df_train = pd.read_csv(data_path, encoding='ISO-8859-1')

    # remove null
    if df_train.isnull().values.any():
        print(df_train.isnull().sum())
        df_train = df_train.dropna()

    # remove empty
    X_train = df_train['text']
    X_train.apply(process_text)
    y_train = df_train["label"]

    c = 10
    print("model path: ", model_path)
    ft = gensim.models.KeyedVectors.load_word2vec_format(model_path, encoding="ISO-8859-1")
    print("vectors")
    vectorizer = Word2VecVectorizer(ft)
    Xtrain = vectorizer.fit_transform(X_train)

    linear = LinearSVC(C=c, penalty='l2', loss='squared_hinge')

    linear.fit(Xtrain, y_train)

    # classification report
    # get_classification_report(vectorizer, linear)

    return vectorizer, linear


def get_classification_report(vectorizer, model):
    df_test = pd.read_csv('data/test_df.csv', encoding='ISO-8859-1')
    df_test.text.apply(process_text)
    data = df_test.text
    data = vectorizer.transform(data)
    y_pred = model.predict(data)
    y_true = df_test.label
    print(y_pred)
    report = classification_report(y_true, y_pred)
    print(report)


def get_model():
    global model
    global vectorizer
    if not model:
        print("model 1st loading")
        vectorizer, model = build_model()
        print("model loaded")
        # print("model ",)
    return vectorizer, model


def screen(text):
    print(text)
    text = process_text(text)
    text = [text]

    print("data: ", text)
    try:
        vectorizer, model = get_model()
        print("model exist: ", (False if not model else True))

        data = vectorizer.transform(text)
        pred = model.predict(data)
        print(model)
        print("prediction: ", pred)
        return SENTIMENT_NAMES[pred[0]]

    except (RuntimeError, TypeError, FileNotFoundError) as err:
        print("err: ", err)
        return ""

