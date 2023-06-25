from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import torch
import numpy as np
import re
task = 'sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
CLASS_NAMES = ["negative", "neutral", "positive"]


def preprocess_text(text) -> str:
    new_text = []
    TAG_RE = re.compile(r'<[^>]+>')

    sentence = str(text)

    # Removing html tags
    sentence = TAG_RE.sub('', sentence)

    # remove non words
    sentence = re.sub(r"[^\w\s\']", "", sentence)

    # Multiple spaces removal
    sentence = re.sub(r" +", ' ', sentence)

    # Removing multiple spaces &
    for word in sentence.split(" "):
        word = '@user' if word.startswith('@') and len(word) > 1 else word
        word = 'http' if word.startswith('http') else word
        new_text.append(word)
    return " ".join(new_text)


# def get_prediction(text, tokenizer, model) -> str:
#     print("text:", text)
#     class_names = ["negative", "neutral", "positive"]
#     text = preprocess_text(text)
#     encoded_input = tokenizer(text, return_tensors='pt')
#     output = model(**encoded_input)
#     scores = output[0][0].detach().numpy()
#
#     scores = softmax(scores)
#     pred = class_names[np.argmax(scores)]
#     return pred


def screen(text) -> str:
    text = preprocess_text(text)
    print(text)
    print(type(text))

    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained(MODEL)
    print("model")
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    print("tokenizer")
    encoded_input = tokenizer(text, return_tensors='pt')
    print("encoded input")
    output = model(**encoded_input)
    print(output)
    scores = output[0][0].detach().numpy()
    print(scores)
    scores = softmax(scores)
    print(scores)
    pred = CLASS_NAMES[np.argmax(scores)]
    print(pred)
    return pred
