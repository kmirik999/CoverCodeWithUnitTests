import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from user_status_checker import UserStatusChecker


class TestUserStatusChecker(unittest.TestCase):
    def setUp(self):
        self.api_url = "https://mock.api.com"
        self.checker = UserStatusChecker(self.api_url)

    def test_fetch_user_data_should_return_data_on_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"data": [{"nickname": "user1"}]}'
        with patch('requests.get', return_value=mock_response):
            user_data = self.checker.fetch_user_data(0)
        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['nickname'], "user1")

    def test_fetch_user_data_should_return_empty_list_on_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 404
        with patch('requests.get', return_value=mock_response):
            user_data = self.checker.fetch_user_data(0)
        self.assertEqual(len(user_data), 0)

    def test_calculate_time_difference_should_return_datetime_objects(self):
        last_seen_str = "2023-09-27T10:00:00Z"
        last_seen_datetime, current_datetime = self.checker.calculate_time_difference(last_seen_str)
        self.assertIsInstance(last_seen_datetime, datetime)
        self.assertIsInstance(current_datetime, datetime)

    def test_print_user_info_should_handle_online_user(self):
        user = {"nickname": "user1", "isOnline": True, "lastSeenDate": "2023-09-27T10:00:00Z"}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user1 is online")



if __name__ == '__main__':
    unittest.main()
