import json
import requests
from datetime import datetime, timezone
from dateutil.parser import parse
import unittest
from unittest.mock import MagicMock, patch


class UserStatusChecker:
    def __init__(self, url, initial_offset=0):
        self.url = url
        self.offset = initial_offset

    def fetch_user_data(self, offset):
        response = requests.get(self.url, params={'offset': offset}, headers={'accept': 'application/json'})
        if response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return []
        json_data = json.loads(response.text)
        return json_data.get('data', [])

    def calculate_time_difference(self, last_seen_str):
        last_seen_datetime = parse(last_seen_str) if last_seen_str else None
        current_datetime = datetime.now(timezone.utc)
        return last_seen_datetime, current_datetime

    def print_user_info(self, user):
        last_seen_str = user['lastSeenDate']
        last_seen_datetime, current_datetime = self.calculate_time_difference(last_seen_str)

        print("...............")
        if user['isOnline']:
            print(f"{user['nickname']} is online")
        elif last_seen_datetime is None:
            print(f"{user['nickname']} has no last seen date")
        else:
            seconds = (current_datetime - last_seen_datetime).total_seconds()
            if 0 <= seconds <= 30:
                print(f"{user['nickname']} seen just now")
            elif 31 <= seconds <= 60:
                print(f"{user['nickname']} seen less than a minute ago")
            elif 61 <= seconds <= 3540:
                print(f"{user['nickname']} seen a couple of minutes ago")
            elif 3541 <= seconds <= 7140:
                print(f"{user['nickname']} seen an hour ago")
            elif last_seen_datetime.day == current_datetime.day and seconds > 7141:
                print(f"{user['nickname']} seen today")
            elif last_seen_datetime.day == current_datetime.day - 1 and seconds > 7141:
                print(f"{user['nickname']} seen yesterday")
            elif 1 < current_datetime.day - last_seen_datetime.day <= 7 and seconds > 7141:
                print(f"{user['nickname']} seen this week")
            else:
                print(f"{user['nickname']} seen long time ago")

    def print_users(self):
        while self.offset < 217:
            user_list = self.fetch_user_data(self.offset)
            for user in user_list:
                self.print_user_info(user)
            self.offset += 50


class TestUserStatusChecker(unittest.TestCase):
    def setUp(self):
        # Create a UserStatusChecker instance with a mock API URL
        self.api_url = "https://mock.api.com"
        self.checker = UserStatusChecker(self.api_url)

    def test_fetch_user_data_success(self):
        # return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"data": [{"nickname": "user1"}]}'
        with patch('requests.get', return_value=mock_response):
            user_data = self.checker.fetch_user_data(0)
        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['nickname'], "user1")

    def test_fetch_user_data_failure(self):
        # return a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        with patch('requests.get', return_value=mock_response):
            user_data = self.checker.fetch_user_data(0)
        self.assertEqual(len(user_data), 0)

    def test_calculate_time_difference(self):
        last_seen_str = "2023-09-27T10:00:00Z"
        last_seen_datetime, current_datetime = self.checker.calculate_time_difference(last_seen_str)
        self.assertIsInstance(last_seen_datetime, datetime)
        self.assertIsInstance(current_datetime, datetime)

    def test_print_user_info_online(self):
        user = {"nickname": "user1", "isOnline": True, "lastSeenDate": "2023-09-27T10:00:00Z"}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user1 is online")

    def test_print_user_info_no_last_seen(self):
        user = {"nickname": "user2", "isOnline": False, "lastSeenDate": None}
        with patch('builtins.print') as mock_print:
            self.checker.print_user_info(user)
        mock_print.assert_called_with("user2 has no last seen date")


url = "https://sef.podkolzin.consulting/api/users/lastSeen"
checker = UserStatusChecker(url)
checker.print_users()

if __name__ == '__main__':
    unittest.main()
