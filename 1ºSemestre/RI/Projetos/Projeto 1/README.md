# Information Retrieval 1s Assignment

In this assignment, we implemented a complete information retrieval system capable of indexing and searching a given document collection. This project gave us hands-on experience with core IR concepts, including document parsing, tokenization, indexing algorithms, and search ranking models. The following image gives an overview of the components that we implemented for the Information Retrieval System:

### Grade: 16.9

![IR Architecture](./images/ir_architecture.png)

## Documentation

### Tokenizer

The `Tokenizer` class is responsible for preprocessing the text of a document by transform it into a list of normalized tokens. This tokens are preprocessed through several steps, including:

- Case normalization;
- Stopword removal, based on a list of stopwords;
- Minimum length filtering;
- Apply stemming.

This class is subdivided into 4 functions:

#### 1. Class initialization (`__init__` function)

```python
def __init__(self, min_token_length=3, normalize_case=True, use_stemming=False, stopwords_file="../data/stop_words.txt"):
```

<ins>**Parameters:**</ins>

- `min_token_length` - Specifies the minimum length a token must have to be retained;
- `normalize_case` - Controls wheter tokens are converted to lowercase for uniformity;
- `use_stemming` - Enables or disables stemming of tokens;
- `stopwords_file` - Specifies the path toa file containing stopwords to ignore during tokenization;

The first step of this function is to create a list containing stopwords, where if specific file is provided, then it's content is stored in a `set` to avoid repeated words, otherwise, if a file is not provided, then by default the stopwords that are going to be used are present in the file [stop_words.txt](./data/stop_words.txt).

If the variable use_stemming is set to True then an instance of the `Snowball Stemmer` class is created.

#### 2. Token Normalization (`normalize_tokens`function)

```python
def normalize_tokens(self, tokens) -> list:
```

This function applies a series of transformations to clean and filter tokens:

- <ins>**Non-Alphanumeric Removal**</ins> - Regular expressions are used to strip out any character that is neither a letter or a digit, reducing each token to its basic alphanumeric form;
- <ins>**Case Normalization**</ins> - If `normaliza_case` is set to **True**, then the token is converted to lowercase;
- <ins>**Length Filtering**</ins> - Tokens shorter than `min_token_length` are discarded. By default this variable has the value **3**;
- <ins>**Stopword Removal**</ins> - Any token found in the stopwords set is ignored;
- - <ins>**Stemming**</ins> - If stemming is enabled, the `SnowballStemmer` is applied to reduce each word to its root form, aiding in generalization.

#### 3. Tokenization (`tokenize` method)

```python
def tokenize(self, text) -> list:
```

This function is the entry point for tokenizing a piece of text. It applies initial tokenization and passes the tokens through the normalization function, described above. It uses NLTK's `word_tokenize` to split the input text into tokens based on whitespace and punctuation. After this process the tokens obtained are passed throught the `normalize_tokens` function to apply all transformations.

#### 4. Configuration File Generation (`write_settings_to_configuration_file` function)

```python
def write_settings_to_configuration_file(self):
```

This function writes the tokenizer's configuration settings to a JSON file, called `configs.json`, so that the searcher can create a instance of a Tokenizer with using the same configuration settings.

### Indexer and SPIMI Algorithm

The SPIMI or Single-Pass In-Memory Indexing algorithm is implemented in the following way:

- **Batch Processing**: Documents are processed in blocks defined by `max_docs_block`, by default the value is **10 000** documents. Once this limite is reached, the current block of tokens and postigns is flushed to disk as a _parcial index_;

- **In Memory Structure**: During the processing, the `current_block` variable stores the terms, document ID's, and positional information. This structure enables fast insertion and avoids frequent reallocations in memory.

- **Disk Flushing**: After reaching the document limit, the function `write_partial_index` is called to write to write the in-memory index to disk and clear memory. The process reduces memory load, allowing the program to handle large data collections incrementally.

- **File Merging**: After all the partial indexes are created, the `Merger` class merges the partial indexes into a final index using a _min-heap_ to keep memory use low.

### Merging Algorithm

Th `Merger`class consolidates multiple partial index files created during the indexing process into a single, final index file. This merging process ensures efficient memory usage by only loading essential data at each step. Here's a step-by-step overview of how the merging algorithm works:

1. <ins>**Open all Partial Index Files**</ins> - All the partial index files are opened simultaneously. Each file contains token data in sorter order, allowing for sequential reading;

2. <ins>**Initialize a Min-Heap**</ins> - A _min-heap_ is created to store and manage toknes from each partial index file, which include the token, the index for the file it came from and the postings lists associated with the token. The usage of the heap enables quick access to the smallest token across all files at any given time;

3. <ins>**Load initial tokens into the heap**</ins> - The algorithm reads the first token from each partial file and adds it to the heap;

4. <ins>**Iteratively Merge tokens**</ins> - The algorithm enters a loop where it retrieves the smallest token entry from the heap and adds this token and its postings lists to the `final_index` in memory. If the token appears in multiple partial files, their postings lists are combined under a single term entry for that token in the final index. The next token from the file (from which the smallest token was just removed) is read and added to the heap, maintaining sorted order;

5. <ins>**Flush to Disk Regularly**</ins> - To prevent the in-memory `final_index` from growing to large, the algorithm periodically writes its contents tothe final index file on the disk, this occurs when the size of `final_index` exceeds **250** elements. After flushing the current entries then the `final_index`structured is cleared to move on to the next tokens;

6. <ins>**Close files and finalize index**</ins> - Once all tokens from all files are processed, any remaining tokens in the `final_index` are written to disk. Finally the algorithm closes all partial files, completing the merge process.

### Index file format

The partial index files and the final index file have the same format, where a index is saved as multiple partial JSONL files. Each line represents a dictionary with a single term as the key and its postings (document ID's and positional lists) as the value. This format allows the Merger to process each line as a distinct entry, simplifying memory management when handling large datasets. An example of this format is provided in the following block of code:

```json
{"secondtrimester": {"11005111": [22], "31401613": [146], "9512261": [0, 25, 131]}}
{"secosteroidal": {"22213321": [36]}}
{"secretagogue": {"11108296": [6, 16], "17544318": [15], "225335": [56]}}
{"secretagogues": {"186589": [14], "16042367": [131, 149], "2900024": [3]}}
{"secretary": {"30086017": [461]}}
{"secretase": {"23327526": [33], "24338474": [5, 7, 14, 22, 38, 67, 109, 126, 135], "24699279": [4, 12, 28, 102, 113, 132], "26433932": [103], "23316412": [4, 10, 66], "15177383": [195]}}
{"secretases": {"9497354": [6]}}
```

```json
{"token1": {"doc1": [position1, position2], "doc2": [position1, position2]}}
{"token2": {"doc3": [position1, position2], "doc4": [position1]}}
```

The token is the term being indexed, is the main key of the dictionary and the postings list is a dictionary with document ID's as keys and lists of positions as values, representing where each term appears within each document.

### Experiments

Some experiments were conducted with different configurations in order to see the impact of each option in the final index. For all the experiments the dataset `MEDLINE_2024_Baseline.jsonl` was used

| Experiment |   normalize case   |      stemming      | max docs per block | minimn token length |
| :--------: | :----------------: | :----------------: | :----------------: | :-----------------: |
|  config 0  | :white_check_mark: |        :x:         |       10000        |          3          |
|  config 1  | :white_check_mark: | :white_check_mark: |       10000        |          3          |
|  config 2  |        :x:         | :white_check_mark: |       10000        |          3          |
|  config 3  |        :x:         |        :x:         |       10000        |          3          |
|  config 4  | :white_check_mark: |        :x:         |        8000        |          2          |
|  config 5  | :white_check_mark: |        :x:         |       12000        |          4          |

The results can be checked in the following table:

| Experiment |  Indexing time  |  Merging Time  | Nº partial index files per minute | Size of the final index | Size of each partial index | Nº index segments |
| :--------: | :-------------: | :------------: | :-------------------------------: | :---------------------: | :------------------------: | :---------------: |
|  config 0  | 7min 59s 472ms  | 1 min 34s 98ms |                 6                 |        897.4 MB         |          18.9 MB           |        50         |
|  config 1  | 13min 53s 278ms | 1min 23s 543ms |                 3                 |         854.8MB         |           17.8MB           |        50         |
|  config 2  | 13min 44s 667ms | 1min 21s 624ms |                 4                 |         854.8MB         |           17.9MB           |        50         |
|  config 3  | 8min 00s 019ms  | 1min 31s 998s  |                 6                 |          920MB          |           19.5MB           |        50         |
|  config 4  | 7min 46s 573ms  | 1min 53s 948s  |                 8                 |         922.2MB         |           15.8MB           |        62         |
|  config 5  | 7min 36s 432ms  | 1min 40s 438ms |                 5                 |         830.9MB         |           21.3MB           |        41         |

#### Indexing and Merging Time

**Config 5** had the shortest indexing time, closely followed by **Config 5**, suggesting that reducing the minimun token length and applying snormalization may slightly improve the indexing time

**Config 1** and **Config 2** experienced longer indexing times, indicating that enabling stemming contributes to slower indexing processes

The **Merging Time** was relatively consistent across all configurations, with only slight variations. The merging time seems unaffect by changes in the configuration options like stemming or normalization

#### Partial Index Efficiency

**Config 0** and **Config 3** produced 6 partial index files per minute, suggesting an efficient process for handling data indexing.

**Config 4** was the most efficient at generating partial index files, producing 8 files per minute, likely due to the smaller block size (8000 docs) and a minimum token length of 2.

**Config 1** and **Config 2** showed reduced partial indexing speed with 3-4 files per minute, because of the additional processing introduced by stemming.

#### Final Index Size

The size of the final index varied slightly across configurations, with **Config 3** producing the largest index at 920MB, while **Config 5** resulted in the smallest final index size of 830.9MB. This indicates that block size and token length influence the final index size, with smaller block sizes and greater token lengths leading to more compact indices, but it may lead to loss of information depending on the minimum token length.

Configurations with stemming (**Config 1** and **Config 2**) produced slightly smaller index sizes (854.8MB), suggesting stemming might reduce the index size by removing word variations.

#### Size of Partial Indexes

**Config 5** had the largest partial index size (21.3MB), which is attributed to the larger block size (12000 docs).

**Config 4** had the smallest partial index size (15.8MB), which aligns with its smaller block size (8000 docs) and leads to more efficient storage and faster merging.

#### Number of Index Segments

**Config 4** generated the most index segments (62 segments), due to the smaller block size and shorter token length, requiring more splits to manage the data efficiently.

**Config 5** had the fewest segments (41 segments), which is a result of the larger block size (12000 docs), leading to fewer but larger segments.

To obtain a list containing several stopwords executed the following code:

```python
from nltk.corpus import stopwords

s = stopwords.words("english")
with open("./data/stop_words.txt", "w") as f:
    for w in s:
        f.write(f"{w}\n")
```

## Searcher

The searcher is the final part of our solution. It loads the index created by the indexer and ranks user queries. The searcher takes the user query and applies the same rule that are applied to the indexer (p.e. tokenization).
The algorithm is composed by 2 main parts:

- The search algorithm
- The ranking algorithm

### Loading the index (`load_index` function)

The main purpose of this function is to load the index into the `Search` class. It reads the index line per line and saves it into the class.

Along with saving the index, this function also calculates the document lengths that will be used for BM25 algorithm during the ranking phase.

```python
# Calculate document lengths for BM25
for doc_id, positions in postings.items():
    doc_length = len(positions)

    if doc_id in doc_lengths:
        doc_lengths[doc_id] += doc_length

    else:
        doc_lengths[doc_id] = doc_length
```

### Search (`search` function)

<ins>_Parameters_</ins>

- `query` - A simple query from a user input. It can be a single term or a _'phrase'_
- `queries_file` - The path to a file containing queries - _'phrases'_ - to be searched

The `Search` class allows for two searching methods: a **single term search** and an **query search**

Based whether the `single_term_index` flag exists, it either searches for a single term or for a query.
The **single term searcher** is the earliest implementation we developed. Although it works, this boolean searcher only returns the posting list for the tokenized searched term. This is implemented by the `search_single_term_index()` function.

The **query search** is implemented by the `search_inverted_index()` function, which within itself calls the `search_query()` function.

#### Query search (`search_query` function)

<ins>_Parameters_</ins>

- `query` - A simple query from the input. It can be a single term or a _'phrase'_
- `query_id` - Query identifier, used when given a `queries_file` on the searcher

The `search_query` method processes the input query by tokenizing it using the `Tokenizer` object and initializing a dictionary called `scores` to store relevance scores for each document.

If **BM25** is used (`use_bm25` flag is `True`), it iterates over each token in the query, checks if the token exists in the index, retrieves the postings list, computes BM25 scores, and accumulates these scores in the `scores` dictionary. If BM25 is not used, the method computes `TF-IDF` scores for the tokens.

After computing the scores, the documents are ranked based on their **scores in descending order**, and the top documents are selected based on a predefined maximum response length (`self.max_response_length`). The results are then saved using the `save_results` method, which formats the output and specifies the output directory:

```python
def save_results(self, query_id, query_text, results):
    """Save search results in memory"""

    output_data = {
        "id": query_id,
        "question": query_text,
        "retrieved_documents": results
    }

    print("Output Data: ", output_data)

    output_file = f"{self.out_dir}/ranked_questions.jsonl"
    with open(output_file, "a") as f:
        json.dump(output_data, f)
        f.write("\n")
```

### Ranking

As we saw in the `search_query()` function, we calculate the scores for each result fetched from the index.

To rank the terms, we use on out of two algorithms: **BM25** or **TF-IDF**.

#### TF-IDF

The TF-IDF (Term Frequency-Inverse Document Frequency) algorithm is used to evaluate the importance of a word in a document relative to a collection of documents (corpus). The `compute_tf_idf_score` method in the `SearchEngine` class computes the TF-IDF scores for the query tokens.

The method processes the input query by **tokenizing** it using the `Tokenizer` and initializing a dictionary called `scores` to store relevance scores for each document.

It iterates over each token in the query, checks if the token exists in the index, retrieves the document frequency (`df`) of the token from `self.doc_freq`, and calculates the **Inverse Document Frequency (IDF)** using the formula:

$$
idf = \log\left(\frac{N}{df + 1} + 1\right)
$$

where `N` is the total number of documents.

For each document in the postings list of the token, the **Term Frequency** (TF) is calculated as the length of the positions list. The TF-IDF score is computed using the formula:

$$
\text{tf\_idf} = (1 + \log(\text{tf})) \times \text{idf}
$$

where `tf` is the term frequency and `idf` is the inverse document frequency.

The TF-IDF score is then multiplied by the count of the token in the query (`query_counter[token]`) and added to the `scores` dictionary for the corresponding document. The method returns the `scores` dictionary containing the TF-IDF scores for each document.


#### BM25 (`BM25` class)

The BM25 algorithm is an improvement over the traditional TF-IDF model and considers term frequency, inverse document frequency, and document length normalization.

It is based on the probabilistic retrieval framework and is used by search engines to **rank documents**. It computes a relevance score for each document based on the following steps:

1. **Initialization**:
   <ins>**Parameters**</ins>

   - `k1` and `b` - term frequency saturation and document length normalization.
   - `avg_doc_length` - average length of documents in the corpus.
   - `doc_lengths` - length of each document.
   - `N` - total number of documents in the corpus.

2. **Setting Document Statistics**:

   The `set_document_stats` method takes a dictionary of document lengths and calculates the average document length.

3. **Computing Inverse Document Frequency (IDF)**:

    The `compute_idf` method calculates the IDF for a term based on its document frequency (`df`) using the formula:

    $$
    \text{idf} = \log\left(1 + \frac{N - df + 0.5}{df + 0.5}\right)
    $$

4. **Computing BM25 Score**:
    The `compute_score` method calculates the BM25 score for a term across all documents in the postings list. For each document, it calculates the term frequency (`tf`) and normalizes it using the formula:

    $$
    \text{norm\_tf} = \left( \frac{tf \cdot (k1 + 1)}{tf + k1 \cdot (1 - b + b \cdot \left( \frac{\text{doc\_length}}{\text{avg\_doc\_length}} \right))} \right)
    $$
    
    The final score for each document is computed as `score = idf * norm_tf`.



## Experiments
We did some experiments with different configurations to observe the impact of using BM25 or TF-IDF on the search and ranking performance. For all the experiments, the dataset `MEDLINE_2024_Baseline.jsonl` was used.

### Experiment Configurations

| Experiment | Use BM25 | Max Response Length |
|------------|----------|---------------------|
| config 0   | ✅       | 100                 |
| config 1   | ❌       | 100                 |

### Results

| Experiment | Total Time | nDCG@10 Score |
|------------|------------|---------------|
| config 0   | 56.590s    | 0.5062        |
| config 1   | 49.700s    | 0.5023        |

### Analysis

**Total Time**:
Config 1 had a slightly shorter total time compared to Config 0, suggesting that using TF-IDF can slightly improve overall performance.
Based on the experiments, the time taken for searching is negligible (the slowest being 7.15e-07s), so the majority of the time is spent on ranking.

**nDCG@10 Score**:
Config 0 achieved a higher nDCG@10 score, suggesting that using BM25 can improve search accuracy compared to TF-IDF.

### Considerations

The experiments show that different configurations can significantly impact the search and ranking performance. Using BM25 generally improves accuracy but can slightly slow down the search process. As the total time difference between BM25 and TF-IDF is over **5 seconds**, and the score difference between the two configurations is not that significant, we opted for using **TF-IDF as the default ranking solution**. BM25 is available as a more accurate yet slower option, accessible via a flag.

## Configuration Options

For our project we developed a CLI using Python's *argparser* package. The following block of code shows the different options available:

```bash
usage: main.py [-h] --mode {index,search} [--input_dir INPUT_DIR] [--output_dir OUTPUT_DIR] [--max_docs_block MAX_DOCS_BLOCK] [--min_token_length MIN_TOKEN_LENGTH] [--normalize_case]
               [--use_stemming] [--stopwords_file STOPWORDS_FILE] [--query QUERY] [--single_term_index] [--index_file INDEX_FILE] [--k1 K1] [--b B] [--use_bm25]
               [--max_response_length MAX_RESPONSE_LENGTH] [--queries_file QUERIES_FILE]

Information Retrieval System CLI

options:
  -h, --help            show this help message and exit
  --mode {index,search}
                        Mode: 'index' to build an index, 'search' to perform search.   # Required
  --input_dir INPUT_DIR
                        Input directory that contains the documents to be analyzed. 
  --output_dir OUTPUT_DIR
                        Output directory for storing the index files.
  --max_docs_block MAX_DOCS_BLOCK
                        Maximum number of documents per block for the indexer (default: 10000).
  --min_token_length MIN_TOKEN_LENGTH
                        Minimum length of tokens to consider (default: 3).
  --normalize_case      Normalize tokens to lowercase.
  --use_stemming        Use stemming to reduce words to their base form.
  --stopwords_file STOPWORDS_FILE
                        File containing a list of stopwords to be removed (one per line).
  --query QUERY         Query string to search for.
  --single_term_index   Use the single-term index for searching.
  --index_file INDEX_FILE
                        Index file name to use for searching.
  --k1 K1               k1 value for the BM25 Ranking algorithm (default: 1.2).
  --b B                 b value for the BM25 Ranking algorithm (default: 0.75).
  --use_bm25            Use the BM25 Ranking algorithm to rank the search results
  --max_response_length MAX_RESPONSE_LENGTH
                        Maximum number of search results to return (default: 100).
  --queries_file QUERIES_FILE
                        Path to a file that contains multiple questions

```

## Execution instructions

To execute our project, we created multiple bash scripts, using different configurations to run either the indexer or the searcher. To run the indexer, it exists 6 scripts that follow the configurations displayed on the table for the indexer experiments:

```bash
.
├── indexer
│   ├── run_config_0.sh
│   ├── run_config_1.sh
│   ├── run_config_2.sh
│   ├── run_config_3.sh
│   ├── run_config_4.sh
│   └── run_config_5.sh
```

To execute them you must simply:

1. Give execution permissions:

```bash
sudo chmod u+x <script> 
```

2. Execute the desired file

```bash
./<script>
```

To run the searcher, 2 files were created, one using the bm25 approach and another based on the SMART algorithm. 

```bash
└── searcher
    ├── run_questions_bm25.sh
    └── run_questions_smart.sh
```

To execute them follow the same instructions mentioned above:



## Conclusion

Our solution has several strengths that we are proud of. The algorithm is optimized for handling large datasets efficiently. When creating the index, we process data in-memory by blocks and write to disk once a determined size is reached. This approach ensures efficient memory usage and faster indexing times.

We also consider our code base to be highly modular, which is crucial for ease of maintenance and bug fixes. The modularity allows different components such as tokenization, indexing, and searching to be extended or modified independently.

The execution times are decent, and considering that our final scores are above 0.50 for the rankers, we can confidently say that our solution is robust. Additionally, we offer extensive customization through various flags, allowing users to tailor the system to their specific needs.

Despite the strengths, we also acknowledge some faults. Occasionally, we encounter duplicate tokens, which isn't ideal. Additionally, our execution times are higher than expected, especially when stemming is enabled.

We have identified several areas for improvement, including developing a more user-friendly CLI. Furthermore, while our current scores are good, we believe there is potential to improve them to exceed 0.70.

Overall, our solution strikes a good balance between performance, accuracy, and flexibility, making it suitable for a wide range of applications.

---

To execute the file you can use the following command

```bash
python3 main.py --mode index --input_dir ../data/MEDLINE_2024_Baseline.jsonl --output_dir ../data/ --stopwords_file ../data/stop_words.txt  --normalize_case
```

To execute the search engine, you can run:

```bash
python3 main.py --mode search --query organization --single_term_index --index /partial_indexes/partial_index_0.jsonl  --output_dir ../data --stopwords_file ../data/stop_words.txt  --normalize_case
```
