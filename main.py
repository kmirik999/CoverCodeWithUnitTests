import json
import requests

url = "https://sef.podkolzin.consulting/api/users/lastSeen"
params = {'offset': 0}


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

    def print_user_info(self, user):
        print("...............")
        if user['isOnline']:
            print(f"{user['nickname']} is online")
        else:
            print(f"{user['nickname']} has no last seen date")

    def print_users(self):
        while self.offset < 217:
            user_list = self.fetch_user_data(self.offset)
            for user in user_list:
                self.print_user_info(user)
            self.offset += 50


checker = UserStatusChecker(url)
checker.print_users()
