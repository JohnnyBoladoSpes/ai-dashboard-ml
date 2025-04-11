import re

import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from .constants import MENTIONS_HASHTAGS_REGEX, PUNCTUATION_REGEX, URLS_REGEX


class TextPreprocessor:
    def __init__(self):
        nltk.download("punkt_tab")
        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text: str) -> str:
        text = re.sub(URLS_REGEX, "", text, flags=re.MULTILINE)
        text = re.sub(MENTIONS_HASHTAGS_REGEX, "", text)
        text = emoji.replace_emoji(text, replace="")
        text = text.lower()
        text = re.sub(PUNCTUATION_REGEX, "", text)
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(w) for w in tokens]
        return " ".join(tokens)
