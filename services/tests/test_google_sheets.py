import unittest
from unittest.mock import MagicMock, patch
from services.google_sheets import GoogleSheets

class TestGoogleSheets(unittest.TestCase):

    def setUp(self):
        self.gs = GoogleSheets()

    def tearDown(self):
        del self.gs

    def test_append_row_success(self):
        # Define test data
        data = {"prompt": "Test prompt", "uuid": "12345"}

        # Create a mock sheet object and authorize the client
        sheet_mock = MagicMock()

        # Call the append_row method
        self.gs.append_row(data)

        # Assert that the append_row method was called with the correct data
        sheet_mock.append_row.assert_called_once_with("Test prompt")

    @patch("builtins.print")
    def test_append_row_failure(self, mock_print):
        # Define test data
        data = {"prompt": "Test prompt", "uuid": "12346"}

        # Create a mock sheet object that raises an error when append_row is called
        sheet_mock = MagicMock()
        sheet_mock.append_row.side_effect = Exception("Test error")

        # Call the append_row method
        self.gs.append_row(data)

        # Assert that the error message was printed to the console
        mock_print.assert_called_once_with("Failed to append row to Google Sheets. Error: Test error")
