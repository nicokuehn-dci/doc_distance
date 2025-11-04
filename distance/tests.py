from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from distance.algo import (
    calculate_similarity_score,
    get_letter_frequencies,
    text_to_list,
    get_frequencies,
)



class TestWordFrequencies(TestCase):
    def test_frequency(self):
        client = APIClient()
        res = client.post(reverse('word-frequencies'), {"payload": ["h", "e", "l", "l", "o"]})
        self.assertDictEqual({'response': {'h': 1, 'e': 1, 'l': 2, 'o': 1}}, res.json())
        self.assertEqual(res.status_code, 200)


class TestTextToList(TestCase):
    def test_words_to_list(self):
        client = APIClient()
        res = client.post(reverse('text-to-list'), {"text": "Hello world, you are awesome"})
        # result is converted to lower case
        self.assertDictEqual({'response': ["hello", "world", "," "you", "are", "awesome"]}, res.json())
        self.assertEqual(res.status_code, 200)


class UnitTest(TestCase):
    def test_similarity(self):
        word = get_letter_frequencies('hello')
        self.assertEqual(calculate_similarity_score(word, word), 1)
        
        word = get_letter_frequencies('hello world, hello')
        word_2 = get_letter_frequencies('hello friends')
        # Test will be refined at a future date
        self.assertTrue(calculate_similarity_score(word, word_2) < 1)


class TestAlgoFunctions(TestCase):
    def test_text_to_list_tokens(self):
        # verify tokenization and normalization behavior
        res = text_to_list('Hello world, you are awesome')
        # current implementation merges punctuation with the following word
        self.assertEqual(res, ["hello", "world", ",you", "are", "awesome"])

    def test_get_frequencies_list_and_string(self):
        self.assertDictEqual(get_frequencies(["h", "e", "l", "l", "o"]), {"h": 1, "e": 1, "l": 2, "o": 1})
        self.assertDictEqual(get_frequencies("hello"), {"h": 1, "e": 1, "l": 2, "o": 1})

    def test_similarity_edge_cases(self):
        # both empty -> 0.0
        self.assertEqual(calculate_similarity_score({}, {}), 0.0)
        # identical dicts -> 1.0
        self.assertEqual(calculate_similarity_score({"a": 2, "b": 1}, {"a": 2, "b": 1}), 1.0)
        # disjoint -> 0.0
        self.assertEqual(calculate_similarity_score({"a": 1}, {"b": 1}), 0.0)

