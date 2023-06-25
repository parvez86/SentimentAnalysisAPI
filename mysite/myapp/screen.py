from transformers import BertTokenizer
from .SentimentClassifier import SentimentClassifier
import re
import torch

PRE_TRAINED_MODEL_NAME = 'bert-base-uncased'
MAX_LENGTH = 160
CLASS_NAMES = ['negative', 'neutral', 'positive']
MODEL_STATE_PATH="model/model_state_cpu.bin"
isFinetuned = False


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

    # Removing multiple spaces & some symbol
    for word in sentence.split(" "):
        word = '@user' if word.startswith('@') and len(word) > 1 else word
        word = 'http' if word.startswith('http') else word
        new_text.append(word)
    return " ".join(new_text)


def screen(data) -> str:
    data = preprocess_text(data)
    # print(data)

    model = SentimentClassifier(3)
    # for loading
    # print(model.state_dict())
    # device = torch.device("cpu")
    # model.to(device)

    global isFinetuned
    if not isFinetuned:
        try:
            model.load_state_dict(torch.load(MODEL_STATE_PATH))
            # see loading optimized train model state
            # print("----loaded----")
            # print(model.state_dict())
            # print("----end load--")
            isFinetuned = True
        except (FileNotFoundError, RuntimeError) as err:
             print("error: ", err)

    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

    encoded_data = tokenizer.encode_plus(
      data,
      add_special_tokens=True,
      max_length=MAX_LENGTH,
      return_token_type_ids=False,
      pad_to_max_length=True,
      return_attention_mask=True,
      return_tensors='pt',
    )
    model.eval()
    outputs = model(
        input_ids=encoded_data['input_ids'],
        attention_mask=encoded_data['attention_mask']
    )
    _, preds = torch.max(outputs, dim=1)
    print(preds)
    return CLASS_NAMES[preds[0]]
