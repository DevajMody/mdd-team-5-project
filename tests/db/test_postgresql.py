import unittest
from tests.test_utils import *


class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        try:
            response = requests.get("http://localhost:8001/manage/version")
            print("Response:", response.status_code, response.text)  # Debug output
            self.assertEqual(response.status_code, 200, f"Response code to /manage/version not 200")
        except Exception as e:
            self.fail(f"Exception occurred: {e}")
