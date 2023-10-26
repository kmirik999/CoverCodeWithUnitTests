import unittest
from data import total_time_in_date_range, minimal_daily_online_time, maximum_daily_online_time, parse_iso8601_datetime, generate_user_report


class IntegrationTests(unittest.TestCase):
    def test_maximum_daily_online_time_integration(self):
        test_user_id = 'a807e6f7-ec9c-f8a6-a6e4-43b8f36c78cc'

        result = maximum_daily_online_time(test_user_id)
        expected_max_daily_time = 32294612.530089002

        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_max_daily_time)[:3])

    def test_minimal_daily_online_time_integration(self):
        test_user_id = 'a807e6f7-ec9c-f8a6-a6e4-43b8f36c78cc'

        result = minimal_daily_online_time(test_user_id)
        expected_min_daily_time = 3056343.642902

        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_min_daily_time)[:3])

    def test_total_time_in_date_range_integration(self):
        test_user_id = '8b0b5db6-19d6-d777-575e-915c2a77959a'
        start_date = '2023-10-08T01:55:38.071188'
        end_date = '2023-10-08T01:57:28.567821'

        start_datetime = parse_iso8601_datetime(start_date)
        end_datetime = parse_iso8601_datetime(end_date)

        expected_total_time = 553.555871
        result = total_time_in_date_range(test_user_id, start_datetime, end_datetime)

        self.assertIsInstance(result, float)
        self.assertEqual(str(result)[:3], str(expected_total_time)[:3])

    def test_generate_user_report_integration(self):
        test_user_ids = ['a807e6f7-ec9c-f8a6-a6e4-43b8f36c78cc', '8b0b5db6-19d6-d777-575e-915c2a77959a']
        test_metrics = ['total_online_time', 'average_times']

        report = generate_user_report(test_user_ids, test_metrics)

        self.assertIsInstance(report, dict)

        for user_id in test_user_ids:
            self.assertIn(user_id, report)

            for metric in test_metrics:
                self.assertIn(metric, report[user_id])
                if metric == 'total_online_time':
                    self.assertIsInstance(report[user_id][metric], float)
                elif metric == 'average_times':
                    self.assertIsInstance(report[user_id][metric], dict)


if __name__ == '__main__':
    unittest.main()
