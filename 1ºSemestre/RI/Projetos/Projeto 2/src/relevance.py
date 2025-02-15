
import math
import json

class RelevanceEvaluator():

    def __init__(self, goldstandard_documents) -> None:
        self.goldstandard_documents = set(item.split(":")[1] for item in goldstandard_documents)

    def get_relevance(self, doc_id) -> int:
        """
            Obtains the relevance score for a document based on whether it exists in the goldstandard_documents.
            - If the document is in the goldstandard, it gets a relevance score (3).
            - Otherwise, it gets a score of 0 (irrelevant).
        """

        if doc_id in self.goldstandard_documents:
            return 1  # Relevant score
        else:
            return 0  # Not relevant

class nDCGCalculator:

    def __init__(self, k=10) -> None:
        self.k = k

    def compute_dcg(self, retrieved_docs, relevance_evaluator: RelevanceEvaluator) -> int:
        """Computes the DCG for the given retrieved documents list."""

        dcg = 0
        for i, doc_id in enumerate(retrieved_docs[:self.k]):

            relevance = relevance_evaluator.get_relevance(doc_id)
            if relevance > 0:
                dcg += relevance / math.log2(i + 2)

        return dcg
        
    def compute_idcg(self, retrieved_docs, relevance_evaluator: RelevanceEvaluator) -> None:
        """
            Computes the IDCG (Ideal DCG) for the given retrieved documents.
            Ideal DCG is the DCG that would occur if all relevant documents were ranked at the top.
        """

        # Sort documents in gold standard order (based on their relevance position)
        ideal_relevance = sorted(retrieved_docs, key=lambda doc_id: relevance_evaluator.get_relevance(doc_id), reverse=True)
        idcg = 0

        for i, doc_id in enumerate(ideal_relevance[:self.k]):
            relevance = relevance_evaluator.get_relevance(doc_id)
            idcg += relevance / math.log2(i + 2)

        return idcg

    
    def compute_ndcg(self, retrieved_docs, goldstandard_documents) -> float:
        """Computes nDCG for the retrieved documents compared to the goldstandard documents."""

        relevance_evaluator = RelevanceEvaluator(goldstandard_documents)
        dcg = self.compute_dcg(retrieved_docs=retrieved_docs, relevance_evaluator=relevance_evaluator)
        idcg = self.compute_idcg(retrieved_docs=retrieved_docs, relevance_evaluator=relevance_evaluator)

        if idcg == 0:
            return 0  # Avoid division by zero if there are no relevant documents
        
        return dcg / idcg

        
    def evaluate_ndcg_for_queries(self, questions_results, questions) -> float:
        """Evaluates the average nDCG for a list of queries."""

        goldstandard_data = {}
        with open(questions, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                query_id = entry["query_id"]
                goldstandard_data[query_id] = entry["goldstandard_documents"]

        total_ndcg = 0
        num_queries = len(questions_results)

        for query_id, retrieved_docs in questions_results.items():
            goldstandard_documents = goldstandard_data.get(query_id)

            ndcg_score = self.compute_ndcg(retrieved_docs=retrieved_docs, goldstandard_documents=goldstandard_documents)
            total_ndcg += ndcg_score  
        
        average_ndcg = total_ndcg / num_queries
        return average_ndcg