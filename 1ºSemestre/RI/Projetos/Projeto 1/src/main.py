
from argparse import ArgumentParser

from corpus_reader import CorpusReader
from tokenizer import Tokenizer
from indexer import Indexer
from search_engine import SearchEngine
from merger import Merger
from relevance import *

import nltk
import os
import json


def main():
    parser = ArgumentParser(description='Information Retrieval System CLI')

    # Main arguments
    parser.add_argument('--mode', choices=['index', 'search'], required=True,
                        help="Mode: 'index' to build an index, 'search' to perform search.")
    
    # Indexer options
    parser.add_argument("--input_dir", type=str, help="Input directory that contains the documents to be analyzed.")
    parser.add_argument("--output_dir", default="../data/", type=str, help="Output directory for storing the index files.")
    parser.add_argument("--max_docs_block", type=int, default=10000, help="Maximum number of documents per block for the indexer (default: 10000).")

    # Tokenizer options
    parser.add_argument("--min_token_length", type=int, default=3, help="Minimum length of tokens to consider (default: 3).")
    parser.add_argument("--normalize_case", default=False, action="store_true", help="Normalize tokens to lowercase.")
    parser.add_argument("--use_stemming", default=False, action="store_true", help="Use stemming to reduce words to their base form.")
    parser.add_argument("--stopwords_file", default="../data/stop_words.txt", type=str, help="File containing a list of stopwords to be removed (one per line).")

    # Search options
    parser.add_argument("--query", type=str, help="Query string to search for.")
    parser.add_argument("--single_term_index", action="store_true", help="Use the single-term index for searching.")
    parser.add_argument("--index_file", default="../data/final_index.jsonl" , type=str, help="Index file name to use for searching.")
    parser.add_argument("--k1", type=int, default=1.2, help="k1 value for the BM25 Ranking algorithm (default: 1.2).")
    parser.add_argument("--b", type=float, default=0.75, help="b value for the BM25 Ranking algorithm (default: 0.75).")
    parser.add_argument("--use_bm25", action="store_true", help="Use the BM25 Ranking algorithm to rank the search results")
    parser.add_argument("--max_response_length", type=int, default=100, help="Maximum number of search results to return (default: 100).")
    parser.add_argument("--queries_file", type=str, help="Path to a file that contains multiple questions")

    args = parser.parse_args()

    if args.mode == 'index':
        run_indexer(args)
    elif args.mode == 'search':
        run_query(args)


def run_indexer(args):
    """Run the indexer with the provided arguments"""

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("punkt not found. Downloading...")
        nltk.download('punkt')

    try:
        nltk.data.find('tokenizers/punkt_data/english.pickle')
    except LookupError:
        print("punkt_tab not found. Downloading...")
        nltk.download('punkt_tab')

    corpus_reader = CorpusReader(
        input_dir=args.input_dir
    )
    
    tokenizer = Tokenizer(
        min_token_length=args.min_token_length,
        normalize_case=args.normalize_case,
        use_stemming=args.use_stemming,
        stopwords_file=args.stopwords_file
    )

    indexer = Indexer(
        tokenizer=tokenizer,
        max_docs_block=args.max_docs_block,
        output_dir=args.output_dir
    )

    merger = Merger(
        partial_indexes_files=indexer.partial_indexes,
        output_dir=args.output_dir
    )

    documents = corpus_reader.read_documents()
    print("Indexing documents....\n")
    for doc_id, doc_text in documents.items():
        indexer.process_document(doc_id=doc_id, text=doc_text)

    print("Finished partial indexing documents\n\nMerging all partial indexes...\n")

    merger.merge_partial_index_files()
    print("Finished merging all partial indexes")


def read_partial_indexes_dir():
    """Read all the partial index files and merge them (function for testing the merge algorithm)"""

    # Read all partial index files from the directory
    partial_indexes_files = [file for file in os.listdir(os.path.join("../data/", "partial_indexes")) if file.endswith(".jsonl")]

    merger = Merger(
        partial_indexes_files=partial_indexes_files,
        output_dir="../data/"
    )

    merger.merge_partial_index_files()


def run_query(args):
    """Run the query with the provided arguments"""

    search_engine = SearchEngine(
        out_dir=args.output_dir, 
        max_response_length=args.max_response_length,
        single_term_index=args.single_term_index, 
        use_bm25=args.use_bm25, 
        index_file=args.index_file,
        k1=args.k1,
        b=args.b
    )

    evaluator = nDCGCalculator()

    search_engine.load_index()

    if args.single_term_index:

        if args.query:
            search_engine.search(query=args.query, queries_file=args.queries_file)

        else:
            raise ValueError("A query string is required when using the single-term index search.")
        
    else:
        search_engine.search(query=args.query, queries_file=args.queries_file)
        print("Finished searching questions")

        results = []

        with open(f"{args.output_dir}/ranked_questions.jsonl", "r") as f:
            for line in f:
                result = json.loads(line.strip())
                results.append(result)

        print("Calculating nDCG@10...")
        average_ndcg = evaluator.evaluate_ndcg_for_queries(questions=args.queries_file, questions_results=results)
        print(f"Average nDCG@10: {average_ndcg:.4f}")


if __name__ == '__main__':
    main()
    # read_partial_indexes_dir()