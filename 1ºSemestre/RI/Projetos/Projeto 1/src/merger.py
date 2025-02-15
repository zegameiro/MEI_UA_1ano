
from collections import defaultdict

import heapq
import os
import json

class Merger:

    def __init__(self, partial_indexes_files, output_dir="../data/"):
        self.partial_indexes_files = partial_indexes_files
        self.output_dir = output_dir
        self.final_index = defaultdict(dict)


    def merge_partial_index_files(self):
        """Merge all partial index files into a single final index file."""

        # Open all partial index files
        files = [open(os.path.join(self.output_dir, "partial_indexes", file), "r") for file in self.partial_indexes_files]

        output_file = f"{self.output_dir}/final_index.jsonl"
        with open(output_file, "w") as f:
            lines_heap = []
            
            # Initialize the heap with the first line from each file
            for i, file in enumerate(files):
                line = file.readline()
                if line:
                    index = json.loads(line.strip())
                    token = list(index.keys())[0]
                    postings = index[token]
                    heapq.heappush(lines_heap, (token, i, postings))

            while lines_heap:
                # Get the smallest token entry across files
                current_token, file_index, current_postings = heapq.heappop(lines_heap)

                self.add_to_final_index(current_token, current_postings)

                next_line = files[file_index].readline()
                if next_line:
                    next_index = json.loads(next_line.strip())
                    next_token = list(next_index.keys())[0]
                    next_postings = next_index[next_token]
                    heapq.heappush(lines_heap, (next_token, file_index, next_postings))

                if len(self.final_index) >= 250:
                    self.update_final_index_file(file=f)

            # Write any remaining entries after processing all lines
            if self.final_index:
                self.update_final_index_file(file=f)

        self.close_partial_index_files(files)


    def add_to_final_index(self, token, postings):
        """Merge postings into the final index for a given token."""

        # Merge each document's postings for the current token
        if token not in self.final_index:
            self.final_index[token] = postings
        else:
            # If the token already exists, merge each document ID and its positions
            for doc_id, positions in postings.items():
                if doc_id in self.final_index[token]:
                    self.final_index[token][doc_id].extend(positions)
                else:
                    self.final_index[token][doc_id] = positions


    def update_final_index_file(self, file) -> None:
        """Write current tokens that are merged to the final index file."""

        for token, postings in self.final_index.items():
            json.dump({token: postings}, file)
            file.write("\n")
        
        self.final_index.clear()


    def close_partial_index_files(self, files) -> None:
        """Close all partial index files."""

        for file in files:
            file.close()

        print(f"Closed {len(files)} partial index files")