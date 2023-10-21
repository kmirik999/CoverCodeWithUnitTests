import subprocess
import unittest


class E2ETest(unittest.TestCase):

    @staticmethod
    def run_application(command, input_data):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=input_data)
        return stdout

    def test_users_online(self):
        command = ["python", "data.py"]

        input_data = "1\n"  # Select the option to count users online
        input_data += "2023-10-08T01:55:38.071188\n"  # Input a date and time

        output = self.run_application(command, input_data)
        self.assertIn("Users online at 2023-10-08 01:55:38.071188: 467", output)

    def test_check_user_presence_at(self):
        command = ["python", "data.py"]

        input_data = "2\n"  # Select the option to check user presence
        input_data += "5ed4eae5-d93c-6b18-be47-93a787c73bcb\n"  # Input a user ID to check
        input_data += "2023-10-08T01:55:01.377022\n"  # Input a date and time in the expected format

        output = self.run_application(command, input_data)
        self.assertIn("User 5ed4eae5-d93c-6b18-be47-93a787c73bcb was online: True", output)

    def test_calculate_total_online_time(self):
        command = ["python", "data.py"]

        input_data = "3\n"  # Select the option to calculate total online time
        input_data += "de5b8815-1689-7c78-44e1-33375e7e2931\n"  # Input a user ID to calculate

        output = self.run_application(command, input_data)
        self.assertIn("Total online time for user de5b8815-1689-7c78-44e1-33375e7e2931:", output)

    def test_calculate_average_times(self):
        command = ["python", "data.py"]

        input_data = "4\n"  # Select the option to calculate average times
        input_data += "de5b8815-1689-7c78-44e1-33375e7e2931\n"  # Input a user ID to calculate average times

        output = self.run_application(command, input_data)

        self.assertIn("Average Daily Time (seconds):", output)
        self.assertIn("Average Weekly Time (seconds):", output)

    def test_total_time_in_date_range(self):
        command = ["python", "data.py"]

        input_data = "6\n"  # Select the option to calculate total time in a date range
        input_data += "8b0b5db6-19d6-d777-575e-915c2a77959a\n"  # Input a user ID to calculate
        input_data += "2023-10-08T01:55:38.071188\n"  # Input the start date and time
        input_data += "2023-10-08T01:57:28.567821\n"  # Input the end date and time

        output = self.run_application(command, input_data)
        self.assertIn("Total time for user 8b0b5db6-19d6-d777-575e-915c2a77959a in the date range:", output)

    def test_minimal_daily_online_time(self):
        command = ["python", "data.py"]

        input_data = "7\n"  # Select the option to calculate minimal daily online time
        input_data += "8b0b5db6-19d6-d777-575e-915c2a77959a\n"  # Input a user ID to calculate

        output = self.run_application(command, input_data)
        self.assertIn("Minimal daily online time for user 8b0b5db6-19d6-d777-575e-915c2a77959a:", output)

    def test_maximum_daily_online_time(self):
        command = ["python", "data.py"]

        input_data = "8\n"  # Select the option to calculate maximum daily online time
        input_data += "8b0b5db6-19d6-d777-575e-915c2a77959a\n"  # Input a user ID to calculate

        output = self.run_application(command, input_data)
        self.assertIn("Maximum daily online time for user 8b0b5db6-19d6-d777-575e-915c2a77959a:", output)

    def test_delete_user_data(self):
        command = ["python", "data.py"]

        input_data = "5\n"  # Select the option to delete user data
        input_data += "697b9b37-a7c7-fec8-c202-c6d6adae5c03\n"  # Input a user ID to delete

        output = self.run_application(command, input_data)
        self.assertIn("User data for user ID 697b9b37-a7c7-fec8-c202-c6d6adae5c03 has been deleted", output)

    def test_generate_user_report(self):
        command = ["python", "data.py"]

        input_data = "9\n"  # Select the option to generate user reports
        input_data += "a807e6f7-ec9c-f8a6-a6e4-43b8f36c78cc,8b0b5db6-19d6-d777-575e-915c2a77959a\n"
        input_data += "total_online_time,average_times\n"

        output = self.run_application(command, input_data)
        self.assertIn("User Report:", output)
        self.assertIn("User ID: a807e6f7-ec9c-f8a6-a6e4-43b8f36c78cc", output)
        self.assertIn("User ID: 8b0b5db6-19d6-d777-575e-915c2a77959a", output)

        self.assertIn("total_online_time", output)
        self.assertIn("average_times", output)


if __name__ == '__main__':
    unittest.main()
