import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def check_blocked_status(github_id):
    creds_base64 = os.environ['GOOGLE_SHEETS_CREDS']
    creds_json_str = base64.b64decode(creds_base64).decode('utf-8')
    creds_json = json.loads(creds_json_str)
    print(creds_json)

    # Convert the dictionary to a credentials object
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

    client = gspread.authorize(creds)
    
    # Use the spreadsheet ID to open the spreadsheet
    spreadsheet_id = os.environ('SPREADSHEET_ID')
    print(spreadsheet_id)
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    # Use the sheet ID (gid) to select the specific sheet
    sheet_id = os.environ('SHEET_ID')
    print(sheet_id)
    sheet = [worksheet for worksheet in spreadsheet.worksheets() if worksheet.id == sheet_id][0]
    
    # Search for the GitHub ID in the sheet
    cell = sheet.find(github_id)
    print(cell)
    print(sheet.row_values(cell.row))
    # Check the status in the corresponding row (assuming status is in Column C)
    isBlocked = sheet.cell(cell.row, 4).value
    
    if isBlocked == "TRUE":
        print(f"::error::User {github_id} is blocked from merging!")
        exit(1)

if __name__ == "__main__":
    github_id = os.environ('GITHUB_ACTOR')
    check_blocked_status(github_id)
