from app.google_api.spreadsheets import SpreadSheets

if __name__ == '__main__':
    ss = SpreadSheets()
    sheet_id = ss.create_spreadsheet()
    print(f'SHEET_ID = {sheet_id}')
