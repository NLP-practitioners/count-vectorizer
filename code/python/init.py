from os import getcwd, listdir
from os.path import abspath, basename, dirname, isfile, join
from typing import Dict, List, TypedDict


class Document(TypedDict):
    filename: str
    tokens: List[str]
    count_vector: Dict[str, int]


def count_vectorize(text):
    # eow = end of word
    eow_punctuations = ["?", ".", "!", ",", "\n", " "]
    eow_punctuations_codes = set([ord(code) for code in eow_punctuations])
    tokens = set()
    count_vector = {}
    token = ''
    for char in text:
        char = char.lower()
        # check end of a token
        if (ord(char) in eow_punctuations_codes):
            if len(token) != 0:
                if not token in tokens:
                    count_vector[token] = 1
                else:
                    count_vector[token] += 1
                tokens.add(token)
                token = ''
        else:
            token += char
    return (count_vector, tokens)


def generate_documents(file_paths: List[str]):
    documents: List[Document] = []
    for file_path in file_paths:
        with open(file_path) as file:
            (count_vector, tokens) = count_vectorize(file.read())
            documents.append({
                "count_vector": count_vector,
                "tokens": tokens,
                "filename": basename(file_path)
            })
    return documents


def generate_vocabulary(documents: List[Document]):
    vocabulary = set()
    for document in documents:
        for token in document["tokens"]:
            vocabulary.add(token)
    return list(vocabulary)


def merge_count_vectors(vocabulary: List[str], documents: List[Document]):
    for document in documents:
        for token in vocabulary:
            if token not in document["count_vector"]:
                document["count_vector"][token] = 0


def main(dataset_directory: str):

    # Get all files in the directory
    file_paths = [join(dataset_directory, f) for f in listdir(dataset_directory)
                  if isfile(join(dataset_directory, f))]

    documents = generate_documents(file_paths)
    vocabulary = generate_vocabulary(documents)
    merge_count_vectors(vocabulary, documents)

    print(documents)


dataset_directory = join(abspath(dirname(__file__)), "..", "..", "datasets")
main(dataset_directory)
