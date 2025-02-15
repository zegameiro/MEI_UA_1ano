from collections import defaultdict
from tokenizer import Tokenizer

import json
import os
import heapq

class Indexer:

    def __init__(self, tokenizer= Tokenizer(), max_docs_block=10000, output_dir="../data/") -> None:
        self.tokenizer = tokenizer
        self.inverted_index = {}
        self.partial_indexes = []
        self.doc_count = 0
        self.max_docs_block = max_docs_block
        self.block_count = 1
        self.output_dir = output_dir if output_dir is not None else "../data/"
        self.current_block = defaultdict(lambda: defaultdict(list))

        self.tokenizer.write_settings_to_configuration_file()


    def process_document(self, doc_id, text) -> None:
        """ Add terms from the tokenized document to the current block (partial index) with positional information"""

        # Tokenize and normalize the text of the document
        tokens = self.tokenizer.tokenize(text=text)

        # Add the term and its positions to the current block's index
        for position, term in enumerate(tokens):
            self.current_block[term][doc_id].append(position) 
        
        self.doc_count += 1

        if self.doc_count >= self.max_docs_block:
            self.write_partial_index()
            self.doc_count = 0
            self.current_block.clear()


    def write_partial_index(self) -> None:
        """Write the current index to the disk as a partial index"""

        block_file = f"partial_index_{self.block_count}.jsonl"
        os.makedirs(f"{self.output_dir}/partial_indexes", exist_ok=True) # Create the directory if it doesn't exist

        block_content = {}

        with open(f"{self.output_dir}/partial_indexes/{block_file}", "w") as f:
            
            tokens_list = list(self.current_block.keys())
            tokens_list.sort()

            for token in tokens_list:
                block_content[token] = self.current_block[token]
                json.dump(block_content, f)
                f.write("\n")
                block_content.clear()
            
            f.close()
            
        print(f"Wrote a partial index to the file partial_index_{self.block_count}.jsonl")

        self.partial_indexes.append(block_file)
        self.block_count += 1

