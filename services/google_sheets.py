import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheets:
    def __init__(self):
        self.scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"), self.scope)
        self.gc = gspread.authorize(self.credentials)

    def append_row(self, data):
        try:
            sheet = self.gc.open("ML Music Video Prompts").sheet1
            sheet.append_row([data["uuid"], data["prompt"], data["timestamp"]])
        except Exception as e:
            print(f"Failed to append row to Google Sheets. Error: {e}")
        finally:
            if hasattr(self.gc, '_http') and hasattr(self.gc._http, 'session'):
                self.gc._http.session.close()
