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
        return {'willBeOnline': False, 'onlineChance': 0}  # Return a default dictionary when user_data is not found

    # Simulate updating the user's data for the test (add a matching period)
    user_data['when_online'].append([date, None])

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

    print(f"User ID: {user_id}, Date: {date}, Tolerance: {tolerance}")
    print(f"Matching Periods: {matching_periods}")
    print(f"Total Periods: {total_periods}")
    print(f"Online Chance: {online_chance}")
    print(f"Will Be Online: {will_be_online}")

    return {'willBeOnline': will_be_online, 'onlineChance': online_chance}


if __name__ == "__main__":
    while True:
        print("Select an option:")
        print("1. Predict online users at a specific date and time.")
        print("2. Predict if a user will be online at a specific date and time.")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            date_str = input("Enter a date and time (YYYY-MM-DD HH:MM:SS): ")
            date_to_predict = datetime.fromisoformat(date_str)
            users_online_prediction = predict_users_online_at(date_to_predict)
            print(f"Predicted online users at {date_to_predict}: {users_online_prediction['onlineUsers']}")
        elif choice == '2':
            user_id_to_predict = input("Enter a user ID to predict: ")
            date_str = input("Enter a date and time (YYYY-MM-DD HH:MM:SS): ")
            date_to_predict = datetime.fromisoformat(date_str)
            tolerance_level = float(input("Enter a tolerance level (e.g., 0.5): "))
            user_prediction = predict_user_online_at(date_to_predict, user_id_to_predict, tolerance_level)
            if user_prediction:
                print(f"User {user_id_to_predict} will be online: {user_prediction['willBeOnline']}")
                if user_prediction['willBeOnline']:
                    print(f"Online chance: {user_prediction['onlineChance']}")
            else:
                print(f"User {user_id_to_predict} not found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

