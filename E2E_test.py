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
        self.assertIn("Users online at 2023-10-08 01:55:38.071188: 491", output)

    def test_check_user_presence_at(self):
        command = ["python", "data.py"]

        input_data = "2\n"  # Select the option to check user presence
        input_data += "de5b8815-1689-7c78-44e1-33375e7e2931\n"  # Input a user ID to check
        input_data += "2023-10-08T01:56:51.608802\n"  # Input a date and time in the expected format

        output = self.run_application(command, input_data)
        self.assertIn("User de5b8815-1689-7c78-44e1-33375e7e2931 was online: True", output)

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


    def test_delete_user_data(self):
        command = ["python", "data.py"]

        input_data = "5\n"  # Select the option to delete user data
        input_data += "de5b8815-1689-7c78-44e1-33375e7e2931\n"  # Input a user ID to delete

        output = self.run_application(command, input_data)
        self.assertIn("User data for user ID de5b8815-1689-7c78-44e1-33375e7e2931 has been deleted", output)


if __name__ == '__main__':
    unittest.main()
