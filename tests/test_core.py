import unittest
from src.database.db_manager import DatabaseManager

class TestSCore(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:") # قاعدة بيانات في الرام للاختبار فقط

    def test_db_logging(self):
        self.db.log_interaction("123", "user", "test message")
        history = self.db.get_chat_history("123")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['role'], 'user')

if __name__ == '__main__':
    unittest.main()

