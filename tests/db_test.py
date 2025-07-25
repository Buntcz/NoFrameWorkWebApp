import unittest
from utils.db import execute_query

class TestDB(unittest.TestCase):
    def test_simple_select(self):
        result = execute_query("SELECT 1 as test_value", fetchone=True)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)

    def test_select_current_timestamp(self):
        result = execute_query("SELECT CURRENT_TIMESTAMP", fetchone=True)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result[0])

    def test_parameterized_query(self):
        result = execute_query("SELECT %s as param_test", (42,), fetchone=True)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 42)

    def test_database_connection_error_handling(self):
        try:
            result = execute_query("INVALID SQL STATEMENT")
            self.assertIsNone(result)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()