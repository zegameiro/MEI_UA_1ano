import json

class CorpusReader:


    def __init__(self, input_dir="../data/MEDLINE_2024_Baseline.jsonl") -> None:
        self.input_dir = input_dir
    

    def read_documents(self) -> dict:
        """Read all the documents that are stored in the data file"""

        documents = {}
        with open(self.input_dir, 'r') as file:
            for line in file:
                document = json.loads(line.strip())
                doc_id = document['doc_id'].split(':')[-1]
                doc_text = document["text"]
                documents[doc_id] = doc_text
        
        return documents
        

