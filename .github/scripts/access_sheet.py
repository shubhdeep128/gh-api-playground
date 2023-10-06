import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def check_blocked_status(github_id):
    creds_json = json.loads(os.environ['GOOGLE_SHEETS_CREDS'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, ["https://spreadsheets.google.com/feeds"])
    
    client = gspread.authorize(creds)
    
    # Use the spreadsheet ID to open the spreadsheet
    spreadsheet_id = os.environ['SPREADSHEET_ID']
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    # Use the sheet ID (gid) to select the specific sheet
    sheet_id = os.environ['SHEET_ID']
    sheet = [worksheet for worksheet in spreadsheet.worksheets() if worksheet.id == sheet_id][0]
    
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
