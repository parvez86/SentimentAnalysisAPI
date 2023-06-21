from datasets import load_dataset
import numpy as np
import pandas as pd
import seaborn as sns
import re
from django.conf import settings

DATASET_NAME = 'Sp1786/multilabel-sentiment-dataset'
# class_names=["negative", "neutral", "positive"]
LABEL_NAMES = ["__label__neg", "__label__neu", "__label__pos"]
DATA_PATH = str(settings.BESE_URL)+'/data'


def draw_count_plot(df, x=None, hue=None):
    counts = df[x].value_counts().to_dict()
    # print(counts)
    if not x and not hue:
        sns.countplot(data=df, x='sentiment', hue="sentiment")


def draw_kde(df, label):
    df[label].plot.kde()


def remove_null(df):
    if df.isnull().values.any():
        print(df.isnull().sum())
        df = df.dropna()

    return df


def pre_process_text(text):
    text = str(text)
    TAG_RE = re.compile(r'<[^>]+>')
    # Removing html tags
    text = TAG_RE.sub('', text)

    # Remove punctuations and numbers
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Single character removal
    sentence = re.sub(r"s+[a-zA-Z]s+", ' ', text)
    text = re.sub(r'[^\w\s\']', '', text)
    text = re.sub(' +', ' ', text).lower()
    # Removing multiple spaces
    sentence = ' '.join([word for word in sentence.split() if len(word) > 1])
    return text


def to_label(df):
    # print(df.shape, df.text.shape)
    for i, v, in df.text.items():
        text = df.text[i];
        if text and text[0] != '_':
            text = LABEL_NAMES[df['label'][i]] + ' ' + v
            # print(i)
            df.text[i] = text
    # print(df)
    return df


def pre_process():
    # load dataset
    ds = load_dataset(DATASET_NAME)

    # splitting dataset
    train_df = pd.DataFrame(ds['train'])
    val_df = pd.DataFrame(ds['validation'])
    test_df = pd.DataFrame(ds['test'])

    # see train data
    # sns.countplot(data=train_df, x='sentiment', hue="sentiment")

    # see validation data
    # sns.countplot(data=val_df, x='sentiment', hue="sentiment")

    # check having null exists
    train_df = remove_null(train_df)
    val_df = remove_null(val_df)
    test_df = remove_null(test_df)


    # if null then drop thats
    # train_df = train_df.dropna()
    # val_df = val_df.dropna()
    test_df = test_df.dropna()  # exists one null data

    # merge 2 df
    df = pd.concat([train_df, val_df])
    # reset index
    df.index = range(0, len(df))
    df.text.to_csv( DATA_PATH+'/train_reviews.csv', index=False, header=False)
    test_df.text.to_csv( DATA_PATH+'/test_reviews.csv', index=False, header=False)
