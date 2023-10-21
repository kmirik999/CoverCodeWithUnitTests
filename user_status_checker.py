import json
import requests
from datetime import datetime, timezone
from dateutil.parser import parse
from Localization import translations


class UserStatusChecker:
    def __init__(self, url, initial_offset=0):
        self.url = url
        self.offset = initial_offset
        self.language = 'en'

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
        translation = translations.get(self.language, translations['en'])
        seconds = None
        if user['isOnline']:
            print(f"{user['nickname']} {translation['online']}")
        elif last_seen_datetime is None:
            seconds = None  # Initialize seconds as None
            print(f"{user['nickname']} {translation['was_online']} {translation['just_now']}")
        else:
            seconds = (current_datetime - last_seen_datetime).total_seconds()
            if seconds is not None:
                if 0 <= seconds <= 30:
                    print(f"{user['nickname']} {translation['just_now']}")
                elif 31 <= seconds <= 60:
                    print(f"{user['nickname']} {translation['less_than_a_minute_ago']}")
                elif 61 <= seconds <= 3540:
                    print(f"{user['nickname']} {translation['a_couple_of_minutes_ago']}")
                elif 3541 <= seconds <= 7140:
                    print(f"{user['nickname']} {translation['an_hour_ago']}")
                elif last_seen_datetime.day == current_datetime.day and seconds > 7141:
                    print(f"{user['nickname']} {translation['today']}")
                elif last_seen_datetime.day == current_datetime.day - 1 and seconds > 7141:
                    print(f"{user['nickname']} {translation['yesterday']}")
                elif 1 < current_datetime.day - last_seen_datetime.day <= 7 and seconds > 7141:
                    print(f"{user['nickname']} {translation['this_week']}")
                else:
                    print(f"{user['nickname']} {translation['a_long_time_ago']}")

        if seconds is None:
            return

    def print_users(self):
        while True:
            user_list = self.fetch_user_data(self.offset)
            if not user_list:
                break
            for user in user_list:
                self.print_user_info(user)
            self.offset += 50

    def set_language(self, language):
        self.language = language


if __name__ == '__main__':
    url = "https://sef.podkolzin.consulting/api/users/lastSeen"
    checker = UserStatusChecker(url)
    checker.set_language('ua')
    checker.print_users()


