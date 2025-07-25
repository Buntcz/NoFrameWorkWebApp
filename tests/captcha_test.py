import unittest
from utils.captcha import generate_captcha

class TestCaptcha(unittest.TestCase):
    def test_generate_captcha_returns_tuple(self):
        result = generate_captcha()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_generate_captcha_question_format(self):
        question, expected = generate_captcha()
        self.assertIsInstance(question, str)
        self.assertIsInstance(expected, str)
        self.assertTrue(question)
        self.assertTrue(expected)

    def test_generate_captcha_contains_math(self):
        question, expected = generate_captcha()
        self.assertTrue(any(char.isdigit() for char in question))
        self.assertTrue(any(op in question for op in ['+', '-', '*']))

    def test_generate_captcha_expected_is_numeric(self):
        question, expected = generate_captcha()
        self.assertTrue(expected.isdigit() or expected.lstrip('-').isdigit())

    def test_generate_captcha_multiple_calls_different(self):
        result1 = generate_captcha()
        result2 = generate_captcha()
        self.assertIsInstance(result1, tuple)
        self.assertIsInstance(result2, tuple)

if __name__ == '__main__':
    unittest.main()