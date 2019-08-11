import re

ORDERED_GUIDE_WORDS = ["is", "are", "they", "it", "he", "she", "the", "a", "be", "been", "has", "have", "go", "went",
                       "to", "of", "who", "on", "not", "for", "when", "that", "which", "and", "or", "but", "do", "does",
                       "at", "this", "from", "would", "one", "so", "up", "an", "will", "won't", "if", "about", "get",
                       "him", "take", "into", "out", "some", "over"]
ENGLISH_CHARS = [c for c in 'abcdefghijklmnopqrstuvwxyz']
TEXT_SPLITTER = re.compile("[.? \n\r!,-@/]")
GUIDE_WORDS = set(ORDERED_GUIDE_WORDS)


def get_tokens(page):
    for raw_token in TEXT_SPLITTER.split(page):
        yield raw_token.lower()


def vectorize(page):
    dict_vector = {key: 0 for key in GUIDE_WORDS}
    english_character_vector = {c: 0 for c in 'abcdefghijklmnopqrstuvwxyz_'}
    total_count = 0
    total_chars = 0
    for token in get_tokens(page):
        total_count += 1
        for ch in token:
            if ch in ENGLISH_CHARS:
                english_character_vector[ch] += 1
            else:
                english_character_vector["_"] += 1
            total_chars += 1
        if token not in GUIDE_WORDS:
            continue
        dict_vector[token] += 1
    result = [dict_vector[guide_word] / total_count if total_count is not 0 else 0 for guide_word in
              ORDERED_GUIDE_WORDS] + [english_character_vector[ch] / total_chars if total_chars is not 0 else 0 for ch
                                      in ENGLISH_CHARS] + [
                 english_character_vector["_"] / total_chars if total_chars is not 0 else 0]
    return result
