from relevance import nDCGCalculator
from tqdm import tqdm

import json
import torch

class Reranker:

    def __init__(self, 
            model, 
            tokenizer, 
            documents: dict, 
            model_path: str,
            ndcg_calculator: nDCGCalculator,
            output_dir: str
        ) -> None:
        """
            Reranker for applying the trained Neural Reranker to new search results.
            :param model: Trained Neural Reranker model instance.
            :param tokenizer: Tokenizer used for the model (e.g., BertTokenizer).
            :param model_path: Path to the saved model weights.
            :param device: Device to run the model on (CPU or GPU).
        """
        
        self.model = model
        self.tokenizer = tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.documents = documents
        self.ndcg_calculator = ndcg_calculator

        # Load the trained model
        self.model.load_state_dict(torch.load(f=model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self.output_dir = output_dir

    def rerank(self, input_file: str, max_length: int = 512):
        """
            Re-rank the search results using the trained Neural Reranker.
            :param input_file: Path to the JSONL file containing the search results.
            :param output_file: Path to save the re-ranked results.
            :param max_length: Maximum sequence length for tokenization.
        """

        print("Re-ranking the search results...")

        reranked_results = []
        unique_questions = []
        seen_queries = set() 

        with open(input_file, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                query_id = data["id"]
                if query_id not in seen_queries:
                    seen_queries.add(query_id)
                    unique_questions.append(data)

        for d in tqdm(unique_questions):
            query_id = d["id"]
            query = d["question"]
            documents = d["retrieved_documents"]

            # Prepare inputs for the model
            doc_scores = []
            for doc_id in documents:
                encoded = self.tokenizer(
                    query,
                    self.documents[f"PMID:{doc_id}"],
                    max_length=max_length,
                    truncation=True,
                    padding="max_length",
                    return_tensors="pt",
                )

                input_ids = encoded["input_ids"].to(self.device)
                attention_mask = encoded["attention_mask"].to(self.device)

                with torch.no_grad():
                    output = self.model(input_ids, attention_mask).logits.item()
                    doc_scores.append((doc_id, output))

            # Sort the documents based on the scores
            doc_scores.sort(key=lambda x: x[1], reverse=True)

            # Keep only the document IDs
            top_documents = [doc[0] for doc in doc_scores[:10]]

            reranked_results.append({
                "id": query_id, 
                "question": query,
                "retrieved_documents": top_documents
            })
        
        # Write the re-ranked results to the final ranked results
        with open(f"{self.output_dir}final_ranked_questions.jsonl", 'w') as file:
            for result in reranked_results:
                file.write(json.dumps(result) + "\n")

    def evaluate_reranker(self, reranked_file: str = "../data/final_ranked_questions.jsonl", goldstandard_file: str = "../../Assignment1/data/questions.jsonl") -> float:
        """
            Evaluate the reranker using nDCG metric.
            :param reranked_file: Path to the re-ranked results.
            :param goldstandard_file: Path to the goldstandard file.
            :return: nDCG score for the re-ranked results.
        """

        questions_results = {}
        with open(reranked_file, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                query_id = entry["id"]
                documents = entry["retrieved_documents"]
                questions_results[query_id] = documents
                
        average_ndcg = self.ndcg_calculator.evaluate_ndcg_for_queries(questions_results, goldstandard_file)
        print(f"Average nDCG@10: {average_ndcg:.4f}")
