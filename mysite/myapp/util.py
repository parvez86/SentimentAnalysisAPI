import re


def process_text(text):
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
