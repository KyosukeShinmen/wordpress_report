from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = config['GoogleAPI']['key_file']
VIEW_ID = config['GoogleAPI']['analytics_view']

def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
  analytics = build('analyticsreporting', 'v4', credentials=credentials)
  return analytics

def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'yesterday'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': [{'name': 'ga:pagePath'}]
        }]
      }
  ).execute()

def makeList(response):
    calc_res = dict()
    pv_summary = []
    report = response.get('reports', [])[0]
    for res in report.get("data",{}).get("rows",[]):
        page_path = res.get('dimensions', [])[0]
        page_path = re.sub(r'\?.+$', '', page_path)
        page_view = int(res.get('metrics', [])[0].get('values')[0])
        if page_path in calc_res:
            calc_res[page_path] += page_view
        else:
            calc_res[page_path] = page_view
    return calc_res    

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  return makeList(response)