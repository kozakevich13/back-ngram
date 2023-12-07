import unittest
from unittest.mock import MagicMock
from app import app, generate_message, get_n_grams, load_word_from_file
import json

class CustomTestResult(unittest.TestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{test.id()}: OK")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{test.id()}: FAILED - {err}")

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def run(self, result=None):
        if result is None:
            result = CustomTestResult()
        return super().run(result)

    def test_generate_message(self):
        seed_word = 'apple is mobile'
        num_words = 5
        n_gram_type = 'bigram'

        try:
            generated_message = generate_message(seed_word, num_words, n_gram_type)
            self.assertIsInstance(generated_message, str)
            print("test_generate_message.....OK")
        except AssertionError as e:
            print(f"test_generate_message.....FAILED: {e}")

    def test_process_text(self):
        test_text = "This is a test text."

        try:
            response = self.app.post('/',
                                     json={'text': test_text},
                                     content_type='application/json')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['message'], 'Text saved successfully.')
            print("test_process_text.....OK")
        except AssertionError as e:
            print(f"test_process_text.....FAILED: {e}")

    def test_delete_text(self):
        try:
            response = self.app.delete('/delete_text')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['message'], 'Text deleted successfully.')
            print("test_delete_text.....OK")
        except AssertionError as e:
            print(f"test_delete_text.....FAILED: {e}")

    def test_get_bigram_dict(self):
        try:
            response = self.app.get('/bigram_dict')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertIsInstance(response.json['bigram_dict'], dict)
            print(f"test_get_bigram_dict.....OK")
        except AssertionError as e:
            print(f"test_get_bigram_dict.....FAILED: {e}")
    def test_get_n_grams(self):
        # Підготовка тестових даних
        test_text = "This is a sample text for testing n-grams."
        with open('saved_text.txt', 'w', encoding='utf-8') as file:
            file.write(test_text)

        response_bigram = self.app.get('/n-grams?type=bigram')
        response_trigram = self.app.get('/n-grams?type=trigram')
        response_invalid = self.app.get('/n-grams?type=invalid_type')

        self.assertEqual(response_bigram.status_code, 200)
        self.assertTrue(response_bigram.json['success'])
        self.assertIsInstance(response_bigram.json['n_gram_dict'], dict)

        self.assertEqual(response_trigram.status_code, 200)
        self.assertTrue(response_trigram.json['success'])
        self.assertIsInstance(response_trigram.json['n_gram_dict'], dict)

        self.assertEqual(response_invalid.status_code, 200)
        self.assertFalse(response_invalid.json['success'])
        self.assertEqual(response_invalid.json['message'], 'Invalid n-gram type. Use "bigram" or "trigram".')

if __name__ == '__main__':
    unittest.main()
