import unittest
from datetime import datetime
from data import count_users_online_at, check_user_presence_at
from predict import predict_users_online_at, predict_user_online_at


sample_data = [
    {
        'userId': '2fba2529-c166-8574-2da2-eac544d82634',
        'isOnline': False,
        'lastSeenDate': '2023-10-07T22:51:51.3880945+00:00',
        'when_online': [],
    },
    {
        'userId': '8b0b5db6-19d6-d777-575e-915c2a77959a',
        'isOnline': True,
        'lastSeenDate': None,
        'when_online': [
            ["2023-10-08T01:55:38.071188", None],
            ["2023-10-08T01:55:50.230817", None],
            # Add more online periods here
        ],
    },
]


class TestYourFunctions(unittest.TestCase):

    def test_should_predict_users_online_at_given_date(self):
        # Test when there is no online user at the specified date
        date_to_test = datetime(2023, 10, 8, 1, 55, 38)
        result = predict_users_online_at(date_to_test)
        self.assertEqual(result['onlineUsers'], 0)

    def test_should_predict_user_online_at_given_date_and_id(self):
        # Test when a user is predicted to be online with high tolerance
        user_id_to_test = '8b0b5db6-19d6-d777-575e-915c2a77959a'
        date_to_test = datetime(2023, 10, 8, 1, 56, 51)
        tolerance_level = 0.9  # High tolerance
        result = predict_user_online_at(date_to_test, user_id_to_test, tolerance_level)
        self.assertTrue(result['willBeOnline'])

    def test_should_count_users_online_at_given_date(self):
        # Test counting users online at a specific date
        date_to_test = datetime(2023, 10, 7, 22, 51, 51)
        result = count_users_online_at(date_to_test)
        self.assertIsInstance(result, int)

    def test_should_check_user_presence_at_given_date(self):
        # Test when the user is present at the specified date
        user_id_to_test = '8b0b5db6-19d6-d777-575e-915c2a77959a'
        date_to_test = datetime(2023, 10, 8, 1, 55, 38)
        result = check_user_presence_at(date_to_test, user_id_to_test)
        self.assertTrue(result['wasUserOnline'])

    def test_should_check_user_presence_at_given_date(self):
        # Test when the user is not present at the specified date
        user_id_to_test = 'e13412b2-fe46-7149-6593-e47043f39c91'
        date_to_test = datetime(2023, 10, 8, 1, 56, 14)  # Use the provided date and time
        result = check_user_presence_at(date_to_test, user_id_to_test)
        self.assertFalse(result['wasUserOnline'])


if __name__ == '__main__':
    unittest.main()
