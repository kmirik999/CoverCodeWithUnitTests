import unittest
from datetime import datetime
from data import check_user_presence_at, count_users_online_at,  calculate_total_online_time, calculate_average_times, delete_user_data, load_full_data
from predict import predict_user_online_at, predict_users_online_at


class TestLastSeen(unittest.TestCase):
    def test_e2e(self):
        # Test check_user_presence_at function
        user_id_to_test = '2fba2529-c166-8574-2da2-eac544d82634'
        date_to_test = datetime(2023, 10, 7, 22, 51, 51)
        result = check_user_presence_at(date_to_test, user_id_to_test)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['wasUserOnline'])

        # Test count_users_online_at function
        date_to_test = datetime(2023, 10, 7, 1, 57, 29)
        result = count_users_online_at(date_to_test)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        # Test predict_user_online_at function
        user_id_to_test = 'de5b8815-1689-7c78-44e1-33375e7e2931'
        date_to_test = datetime(2023, 10, 8, 1, 56, 51)
        tolerance_level = 0.9
        result = predict_user_online_at(date_to_test, user_id_to_test, tolerance_level)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['willBeOnline'])

        # Test predict_users_online_at function
        date_to_test = datetime(2023, 10, 8, 1, 57, 29)
        result = predict_users_online_at(date_to_test)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['onlineUsers'], 1)

        # Test calculate_total_online_time function
        test_user_id = 'de5b8815-1689-7c78-44e1-33375e7e2931'
        result = calculate_total_online_time(test_user_id)
        expected_total_online_time = 1306696.19394
        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_total_online_time)[:3])

        # Test calculate_average_times function
        test_user_id = 'de5b8815-1689-7c78-44e1-33375e7e2931'
        result = calculate_average_times(test_user_id)
        expected_average_daily_time = 186692.15941214285
        expected_average_weekly_time = 1306845.115885
        self.assertEqual(str(result['averageDailyTime'])[:3], str(expected_average_daily_time)[:3])
        self.assertEqual(str(result['averageWeeklyTime'])[:3], str(expected_average_weekly_time)[:3])

        # Test delete_user_data function
        test_user_id_to_delete = '2fba2529-c166-8574-2da2-eac544d82634'
        delete_user_data(test_user_id_to_delete)
        full_data = load_full_data()
        self.assertNotIn(test_user_id_to_delete, [user['userId'] for user in full_data])


if __name__ == '__main__':
    unittest.main()
