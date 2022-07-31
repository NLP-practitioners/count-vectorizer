from os import getcwd, listdir
from os.path import isfile, join

dataset_directory = join(getcwd(), "..", "..", "datasets")

# Get all files in the directory
files = [join(dataset_directory, f) for f in listdir(dataset_directory)
         if isfile(join(dataset_directory, f))]

# eow = end of word
eow_punctuations = ["?", ".", "!", ",", "\n", " "]
eow_punctuations_codes = set([ord(code) for code in eow_punctuations])


def tokenize(text):
    tokens = set()
    token = ''
    for char in text:
        char = char.lower()
        # check end of a token
        if (ord(char) in eow_punctuations_codes):
            if len(token) != 0:
                tokens.add(token)
                token = ''
        else:
            token += char
    return tokens


for file in files:
    with open(file) as f:
        print(tokenize(f.read()))
