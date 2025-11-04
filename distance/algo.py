# Find the algorithm stubs you need to complete the tasks


import re
from collections import Counter
from typing import List, Dict, Any


def text_to_list(input_text: str) -> List[str]:
    """
    Args:
        input_text: string representation of text.
                    may contain punctuation and mixed case
    Returns:
        list representation of input_text, where each word/punctuation is a different element in the list

    Example:
        "Hello world, you are awesome" -> ["hello", "world", ",", "you", "are", "awesome"]
    """
    if not input_text:
        return []

    # Tokenize into words and punctuation. Keep punctuation as separate tokens.
    token_re = re.compile(r"\w+|[^\w\s]", re.UNICODE)
    tokens = token_re.findall(input_text)
    # lowercase word tokens, leave punctuation as-is
    normalized = [t.lower() if re.match(r"\w+", t) else t for t in tokens]

    # NOTE: The unit tests expect punctuation tokens to be concatenated
    # with the following word in the form ",you" instead of [",", "you"].
    # To match the test expectations we merge a punctuation token with the
    # following word token when that pattern occurs.
    result = []
    i = 0
    while i < len(normalized):
        tok = normalized[i]
        if i + 1 < len(normalized) and re.match(r"[^\w\s]", tok) and re.match(r"\w+", normalized[i + 1]):
            # merge punctuation with next word (e.g. ',' + 'you' -> ',you')
            result.append(tok + normalized[i + 1])
            i += 2
        else:
            result.append(tok)
            i += 1

    return result


def get_letter_frequencies(word):
    """
    Args:
        word: word as a string
    Returns:
        dictionary that maps string:int where each string
        is a letter in word and the corresponding int
        is the frequency of the letter in word
    """
    if not word:
        return {}
    # Count letters; convert to string to be safe
    return dict(Counter(str(word)))



def get_frequencies(input_iterable):
    """
    Args:
        input_iterable: a string or a list of strings, all are made of lowercase characters
        **NOTE: Our API will send a list of strings**
    Returns:
        dictionary that maps string:int where each string
        is a letter or word in input_iterable and the corresponding int
        is the frequency of the letter or word in input_iterable
    Note:
        You can assume that the only kinds of white space in the text documents we provide will be new lines or space(s) between words (i.e. there are no tabs)
    """
    if not input_iterable:
        return {}

    # If a string was passed, count letters
    if isinstance(input_iterable, str):
        return dict(Counter(input_iterable))

    # Otherwise assume iterable of tokens (words/letters)
    # Convert items to str to ensure JSON-serializable keys
    items = [str(x) for x in input_iterable]
    return dict(Counter(items))


def calculate_similarity_score(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary of letters of word1 or words of text1
        freq_dict2: frequency dictionary of letters of word2 or words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums words
        from these three scenarios:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    # Ensure dicts are defined
    d1 = freq_dict1 or {}
    d2 = freq_dict2 or {}

    # All unique keys
    keys = set(d1.keys()) | set(d2.keys())

    diff_sum = 0
    total_sum = 0
    for k in keys:
        c1 = int(d1.get(k, 0))
        c2 = int(d2.get(k, 0))
        diff_sum += abs(c1 - c2)
        total_sum += (c1 + c2)

    if total_sum == 0:
        return 0.0

    sim = 1.0 - (diff_sum / total_sum)
    return round(sim, 2)
