import re

class Tokenizer:

    def __init__(self) -> None:
        self.pad_token_id = 0
        self.token_to_id = { "<PAD>": 0 }
        self.vocab_size = len(self.token_to_id)

    def __call__(self, text) -> list[str]:
        """Tokenizes the given text into a list of IDs."""
        
        tokens = text.lower().split(" ")
        token_ids = [self.token_to_id.get(token, self.pad_token_id) for token in tokens]
        return token_ids

    def fit(self, data: list) -> None:
        """Adds to vocabulary dictionary the tokens present in eachdocument"""

        counter = 1
        for text in data:
            tokens = text.split(" ")
            for token in tokens:
                token = re.sub(r'[^a-zA-Z0-9]', ' ', token).strip().lower()
                if token not in self.token_to_id:
                    self.token_to_id[token] = counter
                    counter += 1
                    self.vocab_size += 1