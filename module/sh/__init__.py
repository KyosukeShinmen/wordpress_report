import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
import re
import configparser

ALFABETS = [chr(i) for i in range(65,91)]

class Spread():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        path = os.path.expanduser(config['GoogleAPI']['key_file'])
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        self.sh = gc.open_by_key(config['GoogleAPI']['spreadsheet_name'])
        
    def updateReport(self, table:str, items: list, starts: str = "A2"):
        table = self.sh.worksheet(table)
        y = len(items)
        x = len(items[0])
        num = re.sub("\\D", "", starts)
        end_num = int(num) + int(y)
        area = f"{starts}:{ALFABETS[x-1]}{end_num}"
        table.update(area, items)

    def createReport(self, table: str, items: list, thead = None):
        y = len(items)
        x = len(items[0])
        worksheet = self.sh.add_worksheet(title=table, rows=y+1, cols=x)
        starts = "A1"

        if thead is not None:
            headArea = f"A1:{ALFABETS[x-1]}1"
            worksheet.update(headArea, thead)
            worksheet.format(headArea, {
                "backgroundColor": {
                    "red": 0.1,
                    "green": 0.8,
                    "blue": 1
                },
                "textFormat": {
                    "foregroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 1
                    },
                    "bold": True
                }
            })
            starts = "A2"
            y += 1
        area = f"{starts}:{ALFABETS[x-1]}{y}"
        worksheet.update(area, items)