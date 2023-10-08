import unittest
from datetime import datetime
from data import check_user_presence_at, count_users_online_at
from predict import predict_user_online_at, predict_users_online_at


class IntegrationTests(unittest.TestCase):
    def test_check_user_presence_at_integration(self):
        user_id_to_test = '2fba2529-c166-8574-2da2-eac544d82634'
        date_to_test = datetime(2023, 10, 7, 22, 51, 51)

        result = check_user_presence_at(date_to_test, user_id_to_test)

        self.assertIsInstance(result, dict)
        self.assertFalse(result['wasUserOnline'])  # The user was not online at this date

    def test_count_users_online_at_integration(self):
        date_to_test = datetime(2023, 10, 7, 1, 57, 29)

        result = count_users_online_at(date_to_test)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)  # There should be 1 user online at this date

    def test_predict_user_online_at_integration(self):
        user_id_to_test = 'de5b8815-1689-7c78-44e1-33375e7e2931'
        date_to_test = datetime(2023, 10, 8, 1, 56, 51)
        tolerance_level = 0.9

        result = predict_user_online_at(date_to_test, user_id_to_test, tolerance_level)

        self.assertIsInstance(result, dict)
        self.assertFalse(result['willBeOnline'])  # High tolerance, should be online

    def test_predict_users_online_at_integration(self):
        date_to_test = datetime(2023, 10, 8, 1, 57, 29)

        result = predict_users_online_at(date_to_test)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['onlineUsers'], 1)  # There should be 1 user online at this date


if __name__ == '__main__':
    unittest.main()
