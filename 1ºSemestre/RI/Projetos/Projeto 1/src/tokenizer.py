from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

import re
import os
import json

class Tokenizer:

    def __init__(self, min_token_length=3, normalize_case=True, use_stemming=False,
                 stopwords_file="../data/stop_words.txt") -> None:

        self.min_token_length = min_token_length
        self.stopwords_file = stopwords_file
        self.normalize_case = normalize_case
        self.use_stemming = use_stemming
        self.stopwords = set()

        path, _ = os.path.split(os.path.abspath(__file__)) # Get the directory path of the current file

        if stopwords_file:
            with open(f"{path}/{stopwords_file}", "r") as file:
                self.stopwords = set(w.lower() for w in file.read().split())
        
        self.stemmer = SnowballStemmer("english") if self.use_stemming else None


    def write_settings_to_configuration_file(self):

        with open("configs.json", "w") as config_file:
            config_data = {
                "tokenizer": {
                    "min_token_length": self.min_token_length,
                    "normalize_case": self.normalize_case,
                    "use_stemming": self.use_stemming,
                    "stopwords_file": self.stopwords_file
                }
            }
            json.dump(config_data, config_file)


    def normalize_tokens(self, tokens) -> list:
        """Transform a list that contains multiple tokens into terms"""
        
        normalized_tokens = []

        for token in tokens:

            token = re.sub(r'[^a-zA-Z0-9]', ' ', token).strip()
            token = token.replace(' ', '')

            # Tranform the token to lowercase
            if self.normalize_case:
                token = token.lower()

            # Discard tokens that are shorter than the minimum token length
            if self.min_token_length and len(token) < self.min_token_length:
                continue

            # the token is a stopword and should be discarded
            if self.stopwords and token.casefold() in self.stopwords:
                continue
            
            # Apply stemming if requested
            if self.use_stemming and self.stemmer:
                token = self.stemmer.stem(token)

            normalized_tokens.append(token)

        return normalized_tokens
        

    def tokenize(self, text) -> list:
        """Tokenize and apply transformations based on user settings"""

        # Tokenize the input text
        tokens = word_tokenize(text)

        return self.normalize_tokens(tokens)

        