from transformers import BertTokenizer, BertForSequenceClassification, TFAutoModel, AutoTokenizer
from transformers import pipeline
import re
import torch
import joblib
from django.conf import settings

MODEL_FINE_TUNER_PATH = str(settings.BASE_DIR)+'/model/best_model_state.bin'
isFineTuned = False


def preprocess_text(text) -> str:
    TAG_RE = re.compile(r'<[^>]+>')

    # Removing html tags
    sentence = TAG_RE.sub('', text)

    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
    sentence = re.sub(r"s+[a-zA-Z]s+", ' ', sentence)

    # Removing multiple spaces
    sentence = ' '.join([word for word in sentence.split() if len(word) > 1])
    return sentence


def screen(data) -> str:
    data = preprocess_text(data)
    # print(data)

    model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
    tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")

    global isFineTuned
    if not isFineTuned:
        print("hi")
        # print(settings.BASE_DIR)
        print("Fine tuned parameter: ", model.state_dict())
        print("hi..")
        # model.load_state_dict(joblib.load(MODEL_FINE_TUNER_PATH))
        model.load_state_dict(torch.load(MODEL_FINE_TUNER_PATH))
        print("hi...")
        isFineTuned = True

    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = nlp([data])
    return result[0]['label']
