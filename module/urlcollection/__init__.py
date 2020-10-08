from urllib.parse import urljoin
import sys
import urllib.request
import configparser

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
  def redirect_request(self, req, fp, code, msg, hdrs, newurl):
    self.newurl = newurl
    return None

def domain():
  config = configparser.ConfigParser()
  config.read('config.ini', encoding='utf-8')
  homeURL = config['other']['home']
  elm = homeURL.split("/")[:3]
  domain = "/".join(elm)
  return domain


def createUrlFromPostId(post_id: int):
  config = configparser.ConfigParser()
  config.read('config.ini', encoding='utf-8')
  homeURL = config['other']['home']
  return f"{homeURL}?p={post_id}"

def getRedirectUrl(src_url):
  no_redirect_handler = NoRedirectHandler()
  opener = urllib.request.build_opener(no_redirect_handler)
  try:
    with opener.open(src_url) as res:
      return src_url
  except urllib.error.HTTPError as e:
    if hasattr(no_redirect_handler, "newurl"):
      return no_redirect_handler.newurl
    else:
      raise e

def absolutePath(href: str):
  config = configparser.ConfigParser()
  config.read('config.ini', encoding='utf-8')
  homeURL = config['other']['home']
  if href.startswith("/"):
      return domain()+href
  elif href.startswith("http"):
      return href
  else:
      return urljoin(homeURL, href)