from tokenizer import Tokenizer
from collections import defaultdict, Counter 

import json
import math
import uuid

class BM25:
    
    def __init__(self, k1=1.2, b=0.75) -> None:

        assert 0 <= b <= 1, "The document length normalization (b) must be bigger than 0 and smaller than 1"

        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0
        self.doc_lengths = {}
        self.N = 0 # Total number of  documents in the corpus

    def set_document_stats(self, doc_lengths: dict) -> None:
        """Set document lengths and calculate average document length"""

        self.doc_lengths = doc_lengths
        self.N = len(doc_lengths) 
        self.avg_doc_length = sum(doc_lengths.values()) / len(doc_lengths) 
    
    def compute_idf(self, df: int) -> float:
        """Compute the inverse document frequency for a term"""
        return math.log(1 + (len(self.doc_lengths)  - df + 0.5) / (df + 0.5))

    def compute_score(self, postings) -> dict:
        """Compute BM25 score for a term accross all documents in the postigns list"""

        scores = {}
        df = len(postings) # Document frequency for the term
        idf = self.compute_idf(df)

        for doc_id, positions in postings.items():

            tf = len(positions) # Term frequency in the document
            doc_length = self.doc_lengths[doc_id]

            norm_tf = ((tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))))
            score = idf * norm_tf

            if doc_id not in scores:
                scores[doc_id] = score
            else:
                scores[doc_id] += score

        return scores


class SearchEngine:
    
    def __init__(self, out_dir="../data/", index_file=None, single_term_index=True,
                 max_response_length = 100, k1=1.2, b=1, use_bm25=True) -> None:
        
        self.out_dir = out_dir
        self.index_file = index_file
        self.single_term_index = single_term_index
        self.max_response_length = max_response_length

        # Create a tokenizer considering the one used for the indexing
        self.tokenizer = None
        self.load_configs_file()

        self.index = None
        self.bm25 = BM25(k1=k1, b=b) # Initialize BM25 with customizable parameters
        self.doc_freq = {} # Store document frequency for each term (used for TF-IDF)
        self.use_bm25 = use_bm25

    def load_configs_file(self):
        """Load configurations from a JSON file"""

        with open("configs.json", 'r') as file:
            config_data = json.load(file)

            self.tokenizer = Tokenizer(
                min_token_length=config_data["tokenizer"]["min_token_length"],
                normalize_case=config_data["tokenizer"]["normalize_case"],
                use_stemming=config_data["tokenizer"]["use_stemming"],
                stopwords_file=config_data["tokenizer"]["stopwords_file"]
            )

    def load_index(self):
        """Load the index and document statistics from disk"""

        self.index = {}
        doc_lengths = {}

        print("Loading final index...")

        with open(self.index_file, 'r') as file:

            for line in file:
                entry = json.loads(line.strip())
                token = list(entry.keys())[0]
                postings = entry[token]
                self.index[token] = postings
                self.doc_freq[token] = len(postings)

                # Calculate document lengths for BM25
                for doc_id, positions in postings.items():
                    doc_length = len(positions)

                    if doc_id in doc_lengths:
                        doc_lengths[doc_id] += doc_length

                    else:
                        doc_lengths[doc_id] = doc_length

        # Set document statistics in BM25
        self.bm25.set_document_stats(doc_lengths=doc_lengths)

        print("Finsihed Load Index")

    def search(self, query, queries_file):
        """Search the index for the query terms and return the results"""

        if self.single_term_index:
            self.search_single_term_index(query)
        else:
            self.search_inverted_index(query=query, queries_file=queries_file)
         
    def search_single_term_index(self, query) -> None:
        """ Search the index for the query terms and return the results """

        # Tokenize the query
        tokens = self.tokenizer.tokenize(query)

        # Search the index for the query terms
        results = []
        with open(self.index, "r") as f:
            for line in f:
                line = json.loads(line)
                if line["token"] in tokens:
                    results.extend(line["postings"])

        # Save the results
        
        with open(f"{self.out_dir}/results.txt", "w") as f:
            for result in results[:self.max_response_length]:
                f.write(f"{result}\n")

    def compute_tf_idf_score(self, query_tokens):
        """Compute term frequency and inverted document frequency scores for the query tokens"""

        scores = defaultdict(float)
        query_counter = Counter(query_tokens)

        for token in query_tokens:
            if token in self.index:
                df = self.doc_freq.get(token, 0)
                idf = math.log((len(self.bm25.doc_lengths) / (df + 1)) + 1) # Using smoothed IDF

                postings = self.index[token]
                for doc_id, positions in postings.items():
                    tf = len(positions)
                    tf_idf = (1 + math.log(tf)) * idf # log-scaled tf and idf

                    scores[doc_id] += tf_idf * query_counter[token]

        return scores
    

    def search_inverted_index(self, query=None, queries_file=None):
        """Search for a query in a inverted index file"""

        if query:
            self.search_query(query=query)

        elif queries_file:
            with open(queries_file, 'r') as file:
                for line in file:
                    entry = json.loads(line.strip())
                    question = entry["question"]
                    query_id = entry["query_id"]
                    self.search_query(query=question, query_id=query_id)
        else:
            print("Error you must provide or a query or a query containing multiple ")

    
    def search_query(self, query, query_id=None) -> None:
        """Get the relevant documents associated with a query"""

        tokens = self.tokenizer.tokenize(query)
        scores = defaultdict(float)

        print("Calculating score for query: \"{}\"".format(query))

        if self.use_bm25:

            for token in tokens:

                if token in self.index:

                    postings = self.index[token]
                    term_scores = self.bm25.compute_score(postings=postings)

                    for doc_id, score in term_scores.items():
                        scores[doc_id] += score
                
                else:
                    print(f"Token '{token}' not found in the index.")

        else:
            scores = self.compute_tf_idf_score(tokens)

        # Rank and select top results
        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_docs = [doc_id for doc_id, _ in ranked_results[:self.max_response_length]]

        if query_id:
            self.save_results(query_id=query_id, query_text=query, results=top_docs)
        else:
            self.save_results(query_id=str(uuid.uuid4()), query_text=query, results=top_docs)

        
    def save_results(self, query_id, query_text, results):
        """Save search results in memory"""

        output_data = {
            "id": query_id,
            "question": query_text,
            "retrieved_documents": results
        }

        output_file = f"{self.out_dir}/ranked_questions.jsonl"
        with open(output_file, "a") as f:
            json.dump(output_data, f)
            f.write("\n")

