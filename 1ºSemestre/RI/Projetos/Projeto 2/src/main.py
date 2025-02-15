from transformers import BertTokenizerFast, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
from corpus_reader import CorpusReader
from train_dataset import TrainDataset
from trainer import Trainer
from relevance import nDCGCalculator
from reranker import Reranker

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Train or rerank using a BERT-based model.")

    parser.add_argument("--train_data_path", type=str, default="../data/training_data.jsonl", help="Path to the training data file.")
    parser.add_argument("--bm25_data_path", type=str, default="../data/training_data_bm25_ranked.jsonl", help="Path to the training data BM25 file.")
    parser.add_argument("--documents_path", default="../../Assignment1/data/MEDLINE_2024_Baseline.jsonl", type=str, help="Path to the documents file.")
    parser.add_argument("--use_bert", default=False, action="store_true", help="Use the BERT model.")
    parser.add_argument('--mode', choices=['rerank', 'train'], required=True,
                        help="Mode: 'index' to build an index, 'search' to perform search.")
    parser.add_argument("--ranked_questions_path", default="../../Assignment1/data/ranked_question.jsonl", type=str, help="Path to the ranked questions file.")
    parser.add_argument("--embeddings_path", default="../data/best_model.pth", type=str, help="Path to the embeddings file.")
    parser.add_argument("--output_dir", default="../data/", type=str, help="Output directory to store the final ranked questions file.")

    return parser.parse_args()

def main():
    args = parse_arguments()

    corpus = CorpusReader(input_dir=args.documents_path)
    print("Loading documents...")
    documents = corpus.load_documents()
    
    if args.mode == "train":
        print("Loading training data...")
        training_data = corpus.load_training_data(args.train_data_path)

        print("Loading BM25 training data...")
        bm25_training_data = corpus.load_training_data_bm25(args.bm25_data_path)

        tokenizer = (BertTokenizerFast.from_pretrained("bert-base-uncased")
                     if args.use_bert else
                     AutoTokenizer.from_pretrained("microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"))

        print("Creating training dataset...")
        train_dataset = TrainDataset(
            training_data=training_data,
            bm25_data=bm25_training_data,
            documents=documents,
            tokenizer=tokenizer,
        )

        model = (BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=1)
                 if args.use_bert else
                 AutoModelForSequenceClassification.from_pretrained(
                     "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext", num_labels=1))

        print("Training the model...")
        trainer = Trainer(
            model=model,
            train_dataset=train_dataset,
        )
        trainer.train()

    elif args.mode == "rerank":
        if not args.ranked_questions_path:
            raise ValueError("Path to ranked questions file must be provided for reranking.")

        tokenizer = (BertTokenizerFast.from_pretrained("bert-base-uncased")
                     if args.use_bert else
                     AutoTokenizer.from_pretrained("microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"))

        model = (BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=1)
                 if args.use_bert else
                 AutoModelForSequenceClassification.from_pretrained(
                     "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext", num_labels=1))

        evaluator = nDCGCalculator()
        reranker = Reranker(
            model=model,
            tokenizer=tokenizer,
            documents=documents,
            model_path=args.embeddings_path,
            ndcg_calculator=evaluator,
            output_dir=args.output_dir
        )

        print("Reranking the questions...")
        reranker.rerank(input_file=args.ranked_questions_path)

        output_path = f"{args.output_dir}final_ranked_questions.jsonl"
        reranker.evaluate_reranker(reranked_file=output_path)

if __name__ == "__main__":
    main()