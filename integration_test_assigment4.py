import unittest
from data import calculate_total_online_time, calculate_average_times, delete_user_data, load_full_data


class IntegrationTests(unittest.TestCase):
    def test_calculate_total_online_time_integration(self):
        test_user_id = '8b0b5db6-19d6-d777-575e-915c2a77959a'

        result = calculate_total_online_time(test_user_id)

        expected_total_online_time = 11977136.721496

        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_total_online_time)[:3])

    def test_calculate_average_times_integration(self):
        test_user_id = '8b0b5db6-19d6-d777-575e-915c2a77959a'

        result = calculate_average_times(test_user_id)

        expected_average_daily_time = 1711045.8343238572
        expected_average_weekly_time = 11977320.840267

        self.assertEqual(str(result['averageDailyTime'])[:3], str(expected_average_daily_time)[:3])
        self.assertEqual(str(result['averageWeeklyTime'])[:3], str(expected_average_weekly_time)[:3])

    def test_delete_user_data_integration(self):
        test_user_id_to_delete = '2fba2529-c166-8574-2da2-eac544d82634'

        delete_user_data(test_user_id_to_delete)

        full_data = load_full_data()

        self.assertNotIn(test_user_id_to_delete, [user['userId'] for user in full_data])
