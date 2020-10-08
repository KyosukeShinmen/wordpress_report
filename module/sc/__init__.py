from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import configparser
from datetime import datetime, date, timedelta

class googleSC():
    def __init__(self):

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
        KEY_FILE_LOCATION = config['GoogleAPI']['key_file']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
        self.webmasters = build('webmasters', 'v3', credentials=credentials)
        self.url = config['GoogleAPI']['search_console_url']

    def getResponse(self, body: dict):
        return self.webmasters.searchanalytics().query(siteUrl=self.url, body=body).execute()


    def getQuery(self, daterange: dict = {"start":8, "end":1}):
        today = datetime.today()

        d_list = ['page', 'query']
        start_date = datetime.strftime(today - timedelta(days=daterange['start']), '%Y-%m-%d')
        end_date = datetime.strftime(today - timedelta(days=daterange['end']), '%Y-%m-%d')
        row_limit = 25000

        body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': d_list,
            'rowLimit': row_limit
        }

        response = self.getResponse(body)

        df = pd.io.json.json_normalize(response['rows'])

        for i, d in enumerate(d_list):
            df[d] = df['keys'].apply(lambda x: x[i])

        df.drop(columns='keys', inplace=True)
        df.to_csv('data/{}.csv'.format(start_date), index=False)

        result = {}
        for res in response.get("rows"):
            url = res['keys'][0]
            ranking = f"{res['keys'][1]} : {round(res['position'], 1)}位"
            if url in result:
                result[url].append(ranking)
            else:
                result[url] = [ranking]
                
        for item in result:
            result[item] = "\n".join(result[item])

        return result

