import unicodedata


def normalize(unicode):

    normalized = unicodedata.normalize(
        'NFKD', unicode).encode('ascii', 'ignore').decode()
    return normalized
