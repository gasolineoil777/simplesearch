import re
import os

SEPARATORS = ' |!|"|#|\\$|%|&|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\^|_|`|\\{|\\}|~|\n'
MAX_SCORE = 100
MAX_RESULTS = 10


def extract_words(file, is_sensitive=True):
    f = open(file)
    text = f.read()
    f.close()
    return set(do_split(text, is_sensitive))


def do_split(text, is_sensitive=True):
    return [
        word if is_sensitive else word.lower()
        for word in filter(
            None,
            re.split(SEPARATORS, text)
        )
    ]


def create_index(path, is_sensitive=True):
    try:
        return {
            file: extract_words(os.path.join(path, file), is_sensitive)
            for file in os.listdir(path)
        }
    except FileNotFoundError:
        return {}


def build_results(index, search, is_sensitive=True):
    terms = do_split(search, is_sensitive)
    return dict(
        sorted(
            {
                file: score(terms, words)
                for file, words in index.items()
            }.items(),
            key=lambda item: item[1],
            reverse=True
        )[0:MAX_RESULTS]
    )


def score(terms, words):
    return MAX_SCORE - count_missing_terms(terms, words) * MAX_SCORE / len(terms) if terms else 0


def count_missing_terms(terms, words):
    return len([term for term in terms if term not in words])
