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
MODEL_PATH = str(settings.BASE_DIR)+ '\embeddings\cc.en.300.vec'
# MODEL_PATH = '../embeddings/cc.en.300.vec'
DATA_PATH = str(settings.BASE_DIR) + '\data'
# DATA_PATH = '../data'
SENTIMENT_NAMES = ["negative", "neutral", "positive"]
model = None


def build_model():
    # model = fasttext.load_model(MODEL_PATH)
    # model = fasttext.train_supervised(input=r'train_reviews.csv', label_prefix='__label__')
    model_path = "embeddings/cc.en.300.vec"
    data_path = "data/train_df.csv"

    path_parent = os.path.dirname(os.getcwd())
    # os.chdir( path_parent )
    print("data path: ", data_path)
    df_train = pd.read_csv(data_path, encoding='ISO-8859-1')

    # remove null
    if df_train.isnull().values.any():
        print(df_train.isnull().sum())
        df_train = df_train.dropna()

    # remove empty
    # df_train['text'] = df_train[df_train['text'] != ""]
    print("train data")
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
    return linear


def predict(model, review):
    print("review: ", review)
    pred = model.predict([review])
    print("pred: ", pred)
    return pred


def get_classification_report(model):
    df_test = pd.read_csv('data/test_df.csv', encoding='ISO-8859-1')
    df_test.text.apply(process_text)
    y_pred = model.predict(df_test.text)
    y_true = df_test.label
    print(y_pred)
    report = classification_report(y_true, y_pred)
    print(report)


def get_model():
    global model
    if not model:
        print("model 1st loading")
        model = build_model()
        print("model loaded")
        # print("model ",)
    return model


def screen(text):
    text = process_text(text)
    global model
    if not model:
        print("None")
    else:
        print("model exist")
    model = get_model()
    # test_x = pd.Series(list(text))
    print("data: ", [text])
    print()
    pred = model.predict(text)
    print(model)
    # pred=2
    print("prediction: ", pred)
    return model, SENTIMENT_NAMES[pred]


if __name__ == '__main__':
    model_path = '../embeddings/ccc.en.300.vec'
    model = build_model()
    get_classification_report(model)
    print("Main thread")
