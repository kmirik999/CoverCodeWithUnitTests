import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from user_status_checker import UserStatusChecker


class TestUserStatusChecker(unittest.TestCase):
    def setUp(self):
        # Create a UserStatusChecker instance with a mock API URL
        self.api_url = "https://mock.api.com"
        self.checker = UserStatusChecker(self.api_url)

# test_<method_or_feature_to_be_tested>_should_<expected_behavior>

    def test_fetch_user_data_should_return_data_on_success(self):
        # return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"data": [{"nickname": "user1"}]}'
        with patch('requests.get', return_value=mock_response):
            user_data = self.checker.fetch_user_data(0)
        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['nickname'], "user1")

    def test_fetch_user_data_should_return_empty_list_on_failure(self):
        # return a failed response
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

    def test_print_user_info_should_handle_user_with_no_last_seen_date(self):
        user = {"nickname": "user2", "isOnline": False, "lastSeenDate": None}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user2 has no last seen date")

    def test_print_user_info_should_handle_user_seen_just_now(self):
        user = {"nickname": "user3", "isOnline": False, "lastSeenDate": str(datetime.now(timezone.utc))}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user3 seen just now")

    def test_print_user_info_should_handle_user_seen_long_time_ago(self):
        last_seen_date = datetime.now(timezone.utc) - timedelta(days=10)
        user = {"nickname": "user4", "isOnline": False, "lastSeenDate": str(last_seen_date)}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user4 seen long time ago")


if __name__ == '__main__':
    unittest.main()
