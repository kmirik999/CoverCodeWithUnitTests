import requests
import json
import csv
import re
from datetime import datetime, timedelta

API_URL = "https://sef.podkolzin.consulting/api/users"


def retrieve_data(offset):
    url = f"{API_URL}/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data.get('data', [])


def amend_user_data(user, prior_state):
    user_id = user['userId']
    is_online = user['isOnline']
    user_entry = next((entry for entry in prior_state if entry['userId'] == user_id), None)

    if user_entry:
        when_online = user_entry.get('when_online', [])
    else:
        when_online = []

    if is_online:
        if not when_online or not when_online[-1][1]:
            when_online.append([datetime.now().isoformat(), None])
    else:
        if when_online and not when_online[-1][1]:
            when_online[-1][1] = datetime.now().isoformat()

    user['when_online'] = when_online

    if user_entry:
        user_entry['when_online'] = when_online
    else:
        prior_state.append(user)

    return user


def retrieve_and_update_data(prior_state):
    offset = 0
    full_data = []
    counter = 0

    while counter <= 1000:
        data = retrieve_data(offset)

        if not data:
            break

        for d in data:
            user = {'userId': d['userId'], 'isOnline': d['isOnline'], 'lastSeenDate': d['lastSeenDate']}
            updated_user = amend_user_data(user, prior_state)

            if updated_user['userId'] not in (user['userId'] for user in full_data):
                full_data.append(updated_user)

        offset += len(data)
        counter += 1

    with open('full_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['userId', 'isOnline', 'lastSeenDate', 'when_online']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for user in full_data:
            when_online_json = json.dumps(
                [[start.isoformat(), end.isoformat()] if end else [start.isoformat(), None]
                 for start, end in user['when_online']]
            )
            writer.writerow([user['userId'], user['isOnline'], user['lastSeenDate'], when_online_json])


def load_full_data():
    full_data = []
    try:
        with open('full_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                when_online = json.loads(row['when_online'])
                when_online_datetime = [
                    (datetime.fromisoformat(start), datetime.fromisoformat(end) if end else None)
                    for start, end in when_online
                ]
                full_data.append({
                    'userId': row['userId'],
                    'isOnline': row['isOnline'],
                    'lastSeenDate': row['lastSeenDate'],
                    'when_online': when_online_datetime
                })
    except FileNotFoundError:
        pass

    return full_data


def count_users_online_at(date):
    full_data = load_full_data()
    users_online = 0

    for user in full_data:
        for start, end in user['when_online']:
            if start <= date <= (end or datetime.now()):
                users_online += 1

    return users_online


def parse_iso8601_datetime(iso8601_str):
    # Extract the date and time part from the input string
    match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})', iso8601_str)
    if match:
        date_time_str = match.group(1)
        try:
            return datetime.fromisoformat(date_time_str)
        except ValueError:
            pass
    return None


def check_user_presence_at(date_to_check, user_id):
    full_data = load_full_data()

    for user in full_data:
        if user['userId'] == user_id:
            for start, end in user['when_online']:
                if start <= date_to_check <= (end or datetime.now()):
                    return {
                        'wasUserOnline': True,
                        'nearestOnlineTime': start if start <= date_to_check else None
                    }
            return {'wasUserOnline': False, 'nearestOnlineTime': None}

    return {'wasUserOnline': False, 'nearestOnlineTime': None}


def calculate_total_online_time(user_id):
    full_data = load_full_data()
    total_online_time = timedelta(seconds=0)

    for user in full_data:
        if user['userId'] == user_id:
            for start, end in user['when_online']:
                if end:
                    total_online_time += end - start
                else:
                    total_online_time += datetime.now() - start

    print(f"DEBUG: User ID: {user_id}")
    print(f"DEBUG: total_online_time: {total_online_time}")

    return total_online_time.total_seconds()


def calculate_average_times(user_id):
    full_data = load_full_data()
    user_online_periods = []

    for user in full_data:
        if user['userId'] == user_id:
            user_online_periods = user['when_online']
            break

    if not user_online_periods:
        return {'averageDailyTime': 0, 'averageWeeklyTime': 0}

    total_weekly_time = timedelta()

    for start, end in user_online_periods:
        if not end:
            end = datetime.now()

        period_duration = end - start
        total_weekly_time += period_duration

    total_weekly_seconds = total_weekly_time.total_seconds()

    average_daily_time = total_weekly_seconds / 7

    print(f"DEBUG: User ID: {user_id}")
    print(f"DEBUG: user_online_periods: {user_online_periods}")
    print(f"DEBUG: total_daily_seconds: {average_daily_time}")
    print(f"DEBUG: total_weekly_seconds: {total_weekly_seconds}")

    return {'averageDailyTime': average_daily_time, 'averageWeeklyTime': total_weekly_seconds}


def delete_user_data(user_id):
    full_data = load_full_data()

    user_data_to_delete = None
    for user in full_data:
        if user['userId'] == user_id:
            user_data_to_delete = user
            break

    if user_data_to_delete:
        full_data.remove(user_data_to_delete)

        with open('full_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['userId', 'isOnline', 'lastSeenDate', 'when_online']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in full_data:
                when_online_json = json.dumps(
                    [[start.isoformat(), end.isoformat()] if end else [start.isoformat(), None]
                     for start, end in user['when_online']]
                )
                writer.writerow({
                    'userId': user['userId'],
                    'isOnline': user['isOnline'],
                    'lastSeenDate': user['lastSeenDate'],
                    'when_online': when_online_json
                })

        print(f"User data for user ID {user_id} has been deleted from full_data.csv.")
    else:
        print(f"User data for user ID {user_id} not found.")


def total_time_in_date_range(user_id, start_date, end_date):
    full_data = load_full_data()
    total_time = timedelta(seconds=0)

    for user in full_data:
        if user['userId'] == user_id:
            for start, end in user['when_online']:
                if start is None:
                    start = datetime.now()
                if end is None:
                    end = datetime.now()
                if start <= end_date and end >= start_date:
                    overlap_start = max(start, start_date)
                    overlap_end = min(end, end_date)
                    total_time += overlap_end - overlap_start

    return total_time.total_seconds()


def minimal_daily_online_time(user_id):
    full_data = load_full_data()
    minimal_daily_time = float('inf')

    for user in full_data:
        if user['userId'] == user_id:
            daily_time = 0
            last_date = None

            for start, end in user['when_online']:
                if start.date() != last_date:
                    if last_date is not None:
                        minimal_daily_time = min(minimal_daily_time, daily_time)
                    last_date = start.date()
                    daily_time = 0

                if end:
                    daily_time += (end - start).total_seconds()
                else:
                    daily_time += (datetime.now() - start).total_seconds()

            # Check the last day
            if last_date is not None:
                minimal_daily_time = min(minimal_daily_time, daily_time)

    return minimal_daily_time


def maximum_daily_online_time(user_id):
    full_data = load_full_data()
    maximum_daily_time = 0

    for user in full_data:
        if user['userId'] == user_id:
            daily_time = 0
            last_date = None

            for start, end in user['when_online']:
                if start.date() != last_date:
                    # Check if this is a new day
                    if last_date is not None:
                        maximum_daily_time = max(maximum_daily_time, daily_time)
                    last_date = start.date()
                    daily_time = 0

                if end:
                    daily_time += (end - start).total_seconds()
                else:
                    daily_time += (datetime.now() - start).total_seconds()

    if last_date is not None:
        maximum_daily_time = max(maximum_daily_time, daily_time)

    return maximum_daily_time


def generate_user_report(user_ids, metrics):
    report = {}

    for user_id in user_ids:
        report[user_id] = {}

        for metric in metrics:
            if metric == 'total_online_time':
                total_time = calculate_total_online_time(user_id)
                report[user_id]['total_online_time'] = total_time
            elif metric == 'average_times':
                average_times = calculate_average_times(user_id)
                report[user_id]['average_times'] = average_times
            elif metric == 'minimal_daily_time':
                min_daily_time = minimal_daily_online_time(user_id)
                report[user_id]['minimal_daily_time'] = min_daily_time
            elif metric == 'maximum_daily_time':
                max_daily_time = maximum_daily_online_time(user_id)
                report[user_id]['maximum_daily_time'] = max_daily_time
            else:
                report[user_id][metric] = "Invalid Metric"

    return report


if __name__ == "__main__":
    while True:
        print("Select an option:")
        print("1. Count users online at a specific date and time.")
        print("2. Check user presence at a specific date and time.")
        print("3. Calculate total online time for a user.")
        print("4. Calculate average daily and weekly time for a user.")
        print("5. Delete user data based on user ID.")
        print("6. Calculate total time a user was online in a date range.")
        print("7. Calculate minimal daily online time for a user.")
        print("8. Calculate maximum daily online time for a user.")
        print("9. Report")
        print("10. Quit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10): ")

        if choice == '1':
            date_str = input("Enter a date and time (YYYY-MM-DDTHH:MM:SS.abcdefZ): ")
            date_to_check = parse_iso8601_datetime(date_str)
            if date_to_check:
                users_online = count_users_online_at(date_to_check)
                print(f"Users online at {date_to_check}: {users_online}")
            else:
                print("Invalid date and time format. Please use 'YYYY-MM-DDTHH:MM:SS.abcdefZ'.")
        elif choice == '2':
            user_id_to_check = input("Enter a user ID to check: ")
            date_str = input("Enter a date and time (YYYY-MM-DDTHH:MM:SS.abcdefZ): ")
            date_to_check = parse_iso8601_datetime(date_str)
            if date_to_check:
                user_presence = check_user_presence_at(date_to_check, user_id_to_check)
                if user_presence:
                    print(f"User {user_id_to_check} was online: {user_presence['wasUserOnline']}")
                    if user_presence['wasUserOnline']:
                        print(f"Nearest online time: {user_presence['nearestOnlineTime']}")
                else:
                    print(f"User {user_id_to_check} not found.")
            else:
                print("Invalid date and time format. Please use 'YYYY-MM-DDTHH:MM:SS.abcdefZ'.")
        elif choice == '3':
            user_id_to_calculate = input("Enter a user ID to calculate total online time: ")
            total_online_time = calculate_total_online_time(user_id_to_calculate)
            print(f"Total online time for user {user_id_to_calculate}: {total_online_time} seconds")
        elif choice == '4':
            user_id_to_calculate = input("Enter a user ID to calculate average times: ")
            average_times = calculate_average_times(user_id_to_calculate)
            print(f"Average Daily Time (seconds): {average_times['averageDailyTime']}")
            print(f"Average Weekly Time (seconds): {average_times['averageWeeklyTime']}")
        elif choice == '5':
            user_id_to_delete = input("Enter the user ID to delete: ")
            delete_user_data(user_id_to_delete)
        elif choice == '6':
            user_id_to_calculate = input("Enter a user ID: ")
            start_date_str = input("Enter the start date and time (YYYY-MM-DDTHH:MM:SS.abcdefZ): ")
            end_date_str = input("Enter the end date and time (YYYY-MM-DDTHH:MM:SS.abcdefZ): ")
            start_date = parse_iso8601_datetime(start_date_str)
            end_date = parse_iso8601_datetime(end_date_str)
            if start_date and end_date:
                total_time = total_time_in_date_range(user_id_to_calculate, start_date, end_date)
                print(f"Total time for user {user_id_to_calculate} in the date range: {total_time} seconds")
            else:
                print("Invalid date and time format. Please use 'YYYY-MM-DDTHH:MM:SS.abcdefZ'.")
        elif choice == '7':
            user_id_to_calculate = input("Enter a user ID: ")
            min_daily_time = minimal_daily_online_time(user_id_to_calculate)
            print(f"Minimal daily online time for user {user_id_to_calculate}: {min_daily_time} seconds")
        elif choice == '8':
            user_id_to_calculate = input("Enter a user ID: ")
            max_daily_time = maximum_daily_online_time(user_id_to_calculate)
            print(f"Maximum daily online time for user {user_id_to_calculate}: {max_daily_time} seconds")
        elif choice == '9':
            user_ids_input = input("Enter a comma-separated list of user IDs: ")
            user_ids = user_ids_input.split(',')
            metrics_input = input("Enter a comma-separated list of metrics (e.g., total_online_time,average_times): ")
            metrics = metrics_input.split(',')

            user_report = generate_user_report(user_ids, metrics)
            print("User Report:")
            for user_id, data in user_report.items():
                print(f"User ID: {user_id}")
                for metric, value in data.items():
                    print(f"{metric}: {value}")
        elif choice == '10':
            break
        else:
            print("Invalid choice. Please enter a valid option (1-10).")
