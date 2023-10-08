from datetime import datetime
from data import load_full_data


def predict_users_online_at(date):
    full_data = load_full_data()
    online_periods = [user['when_online'] for user in full_data]
    online_users_count = 0
    online_periods_count = 0

    for periods in online_periods:
        for start, end in periods:
            if start <= date <= (end or datetime.now()):
                online_users_count += 1
                online_periods_count += 1

    online_users = round(online_users_count / online_periods_count) if online_periods_count else 0
    return {'onlineUsers': online_users}


def predict_user_online_at(date, user_id, tolerance):
    full_data = load_full_data()
    user_data = next((user for user in full_data if user['userId'] == user_id), None)

    if user_data is None:
        return None

    predict_day_of_week = date.weekday()
    predict_time = date.time()

    matching_periods = []

    for start, end in user_data['when_online']:
        is_correct_weekday = start.weekday() == predict_day_of_week
        is_within_time_range = start.time() <= predict_time <= (end or datetime.now()).time()

        if is_correct_weekday and is_within_time_range:
            matching_periods.append((start, end))

    total_periods = user_data['when_online']

    if not total_periods:
        online_chance = 0
    else:
        online_chance = len(matching_periods) / len(total_periods)

    will_be_online = online_chance >= tolerance

    return {'willBeOnline': will_be_online, 'onlineChance': online_chance}


if __name__ == "__main__":
    pass
