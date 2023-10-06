import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def check_blocked_status(github_id):
    creds_json = json.loads(os.environ['GOOGLE_SHEETS_CREDS'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, ["https://spreadsheets.google.com/feeds"])
    
    client = gspread.authorize(creds)
    
    # Assuming the sheet structure is: Column A = GitHub ID, Column B = Team Name, Column C = Status (Blocked/Not Blocked)
    sheet = client.open("MySheet").sheet1
    
    # Search for the GitHub ID in the sheet
    cell = sheet.find(github_id)
    
    # Check the status in the corresponding row (assuming status is in Column C)
    status = sheet.cell(cell.row, 3).value
    
    if status == "Blocked":
        print(f"::error::User {github_id} is blocked from merging!")
        exit(1)

if __name__ == "__main__":
    github_id = os.environ['GITHUB_ACTOR']
    check_blocked_status(github_id)
