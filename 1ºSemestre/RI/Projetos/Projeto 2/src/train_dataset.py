from torch.utils.data import Dataset
from transformers import BertTokenizerFast
from tqdm import tqdm
import random

class TrainDataset(Dataset):

    def __init__ (
        self, 
        training_data, 
        bm25_data, 
        documents, 
        tokenizer: BertTokenizerFast,
        max_length: int = 320,
        ratio: int = 4
    ):
        """
            Dataset for training the Neural Reranker with static hard negatives.
            :param training_data_path: Path to training data JSONL file.
            :param bm25_ranked_path: Path to BM25 ranked data JSONL file.
            :param tokenizer: Tokenizer instance.
        """

        self.data = []
        self.tokenizer = tokenizer

        # Prepare the dataset
        for entry in tqdm(training_data):
            query_id = entry["query_id"]
            query_text = entry["question"]
            goldstandard_documents = set(entry["goldstandard_documents"])
            bm25_docs= bm25_data[query_id]

            # Positive examples
            for doc in goldstandard_documents:
                encoded = tokenizer(
                    query_text,
                    documents[doc],
                    max_length=max_length,
                    truncation=True,
                    padding="max_length",
                    return_tensors="pt"
                )
                
                self.data.append({
                    "input_ids": encoded["input_ids"].squeeze(0),
                    "attention_mask": encoded["attention_mask"].squeeze(0),
                    "label": 1
                })

            # Hard negative examples
            hard_negatives = [doc_entry["id"] for doc_entry in bm25_docs if doc_entry["id"] not in goldstandard_documents]

            # Sample a fixed number of negative examples per positive example
            sampled_negatives = random.sample(hard_negatives, min(len(hard_negatives), ratio * len(goldstandard_documents)))
            
            for doc in sampled_negatives:
                encoded = tokenizer(
                    query_text,
                    documents[doc],
                    max_length=max_length,
                    truncation=True,
                    padding="max_length",
                    return_tensors="pt",
                )
                
                self.data.append({
                    "input_ids": encoded["input_ids"].squeeze(0),
                    "attention_mask": encoded["attention_mask"].squeeze(0),
                    "label": 0,
                })

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]
            