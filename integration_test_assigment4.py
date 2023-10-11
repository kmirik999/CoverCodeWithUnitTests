import unittest
from data import calculate_total_online_time, calculate_average_times, delete_user_data, load_full_data


class IntegrationTests(unittest.TestCase):
    def test_calculate_total_online_time_integration(self):
        test_user_id = 'de5b8815-1689-7c78-44e1-33375e7e2931'

        result = calculate_total_online_time(test_user_id)

        expected_total_online_time = 1271921.308544

        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_total_online_time)[:3])

    def test_calculate_average_times_integration(self):
        test_user_id = 'de5b8815-1689-7c78-44e1-33375e7e2931'

        result = calculate_average_times(test_user_id)

        expected_average_daily_time = 181703.04407771426
        expected_average_weekly_time = 1271921.308544

        self.assertEqual(str(result['averageDailyTime'])[:3], str(expected_average_daily_time)[:3])
        self.assertEqual(str(result['averageWeeklyTime'])[:3], str(expected_average_weekly_time)[:3])

    def test_delete_user_data_integration(self):
        test_user_id_to_delete = '2fba2529-c166-8574-2da2-eac544d82634'

        delete_user_data(test_user_id_to_delete)

        full_data = load_full_data()

        self.assertNotIn(test_user_id_to_delete, [user['userId'] for user in full_data])
