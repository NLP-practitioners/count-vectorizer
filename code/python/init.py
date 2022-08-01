import math
from os import listdir
from os.path import abspath, basename, dirname, isfile, join
from typing import Dict, List, TypedDict

from normalize import normalize


class Document(TypedDict):
    filename: str
    tokens: List[str]
    count_vector: Dict[str, int]


Documents = List[Document]


def count_vectorize(text, analyzer):
    # characters that indicate the end of a token
    eow_punctuations = ["?", ".", "!", ",", "\n", " ", "(", ")"]
    eow_punctuations_codes = set([ord(code) for code in eow_punctuations])
    tokens = set()
    count_vector = {}
    token = ''
    for char in text:
        char = char.lower()
        normalized_char = normalize(char)
        # check end of a token
        if len(normalized_char) != 0:
            is_punctuation = ord(normalized_char) in eow_punctuations_codes
            if (((analyzer == "word" and is_punctuation) or (analyzer == "char" and not is_punctuation))):
                token = normalized_char if analyzer == "char" else token
                if len(token) != 0:
                    if not token in tokens:
                        count_vector[token] = 1
                    else:
                        count_vector[token] += 1
                    tokens.add(token)
                    token = ''
            elif analyzer != "char":
                token += normalized_char
    return (count_vector, tokens)


def generate_documents(file_paths: List[str], analyzer):
    documents: Documents = []
    for file_path in file_paths:
        with open(file_path, encoding="utf-8") as file:
            (count_vector, tokens) = count_vectorize(file.read(), analyzer)
            documents.append({
                "count_vector": count_vector,
                "tokens": tokens,
                "filename": basename(file_path)
            })
    return documents


def generate_vocabulary(documents: Documents):
    vocabulary = set()
    for document in documents:
        for token in document["tokens"]:
            vocabulary.add(token)
    return list(vocabulary)


def merge_count_vectors(vocabulary: List[str], documents: Documents):
    for document in documents:
        for token in vocabulary:
            if token not in document["count_vector"]:
                document["count_vector"][token] = 0


def generate_count_vector_matrix(vocabulary: List[str], documents: Documents):
    count_vector_matrix = []

    for document in documents:
        sparse_count_vector = []
        for token in vocabulary:
            if token in document["count_vector"]:
                sparse_count_vector.append(document["count_vector"][token])
            else:
                sparse_count_vector.append(0)

        count_vector_matrix.append(sparse_count_vector)

    return count_vector_matrix


def normalize_count_vectors(documents: Documents):
    for document in documents:
        total_tokens = 0
        for count in document["count_vector"].values():
            total_tokens += math.pow(count, 2)
        l2_norm = math.sqrt(total_tokens)

        for token, count in document["count_vector"].items():
            document["count_vector"][token] = count / l2_norm


def main(dataset_directory: str):

    # Get all files in the directory
    file_paths = [join(dataset_directory, f) for f in listdir(dataset_directory)
                  if isfile(join(dataset_directory, f))]

    documents = generate_documents(file_paths, "word")
    vocabulary = generate_vocabulary(documents)
    print(vocabulary)
    vocabulary = sorted(vocabulary)
    merge_count_vectors(vocabulary, documents)
    normalize_count_vectors(documents)
    count_vector_matrix = generate_count_vector_matrix(vocabulary, documents)
    print(count_vector_matrix)


dataset_directory = join(abspath(dirname(__file__)), "..", "..", "datasets")
main(dataset_directory)
