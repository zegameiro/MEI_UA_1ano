import json

class CorpusReader:

    def __init__(self, input_dir="../../Assignment 1/data/MEDLINE_2024_Baseline.jsonl") -> None:
        self.input_dir = input_dir
    
    def load_documents(self) -> dict:
        """Read all the documents that are stored in the data file"""

        documents = {}
        with open(self.input_dir, 'r') as file:
            for line in file:
                document = json.loads(line.strip())
                doc_id = document['doc_id']
                doc_text = document["text"]
                documents[doc_id] = doc_text
        
        return documents
    
    def load_training_data(self, training_data_path: str = "../data/training_data.jsonl") -> list[dict]:
        """
            Read all the training data that has this format:
            {"question": "....", "goldstandard_documents": "....", "query_id": "...."}
        """
        
        training_data = []
        with open(training_data_path, "r") as file:
            for line in file:
                data = json.loads(line.strip())
                training_data.append(data)

        return training_data

    def load_training_data_bm25(self, training_data_bm25_path: str = "../data/training_data_bm25_ranked.jsonl") -> dict:
        """
            Load the BM25 ranked data for the training queries.
            The data is stored in a dictionary with the query_id as the key
        """

        bm25_data = {}
        with open(training_data_bm25_path, "r") as file:
            for line in file:
                data = json.loads(line.strip())
                query_id = data["query_id"]
                bm25_data[query_id] = data["retrieved_documents"]

        return bm25_data