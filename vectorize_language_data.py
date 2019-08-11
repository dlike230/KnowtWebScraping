import re

ORDERED_GUIDE_WORDS = ["is", "are", "they", "it", "he", "she", "the", "a", "be", "been", "has", "have", "go", "went"]
TEXT_SPLITTER = re.compile("[.? \n\r!,-@/]")
GUIDE_WORDS = set(ORDERED_GUIDE_WORDS)

def get_tokens(page):
    for raw_token in TEXT_SPLITTER.split(page):
        yield raw_token.lower()

def vectorize(page):
    dict_vector = {key: 0 for key in GUIDE_WORDS}
    total_count = 0
    for token in get_tokens(page):
        total_count += 1
        if token not in GUIDE_WORDS:
            continue
        dict_vector[token] += 1
    return [dict_vector[guide_word] / total_count if total_count is not 0 else 0 for guide_word in ORDERED_GUIDE_WORDS]