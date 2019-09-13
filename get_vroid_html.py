# -*- coding: utf-8 -*-
#
import urllib
import re
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

urls = {
  "yukari": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%B5%90%E6%9C%88%E3%82%86%E3%81%8B%E3%82%8A",
  "maki": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E5%BC%A6%E5%B7%BB%E3%83%9E%E3%82%AD",
  "zunko": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%81%9A%E3%82%93%E5%AD%90",
  "kotonoha": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%90%B4%E8%91%89%E8%8C%9C%E3%83%BB%E8%91%B5",
  "kiri": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%81%8D%E3%82%8A%E3%81%9F%E3%82%93",
  "itako": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%82%A4%E3%82%BF%E3%82%B3",
  "akari": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%B4%B2%E6%98%9F%E3%81%82%E3%81%8B%E3%82%8A"
}

charname = "yukari"
url = urls[charname]

driver.get(url)

# seigaのURLだけ集める
urls_seiga = []
for elem in driver.find_elements_by_css_selector('a.ext'):
  url = elem.get_attribute('href')
  #import pdb; pdb.set_trace()
  if url.startswith('http://seiga.nicovideo.jp/seiga/im'): # user情報は除く
    urls_seiga.append(url)

# import pdb; pdb.set_trace()
# pass

def seigaid(url):
  id = re.sub('http://seiga.nicovideo.jp/seiga/', '', url)
  return id

# htmlを保存する
store_dir = 'seiga-html/' + charname
for seiga in urls_seiga:
  id = seigaid(seiga)
  out_fname = os.path.join(store_dir, "%s.html" % id)
  driver.get(seiga)
  print(seiga)
  time.sleep(1)
  with open(out_fname, 'w') as f:
    html = driver.page_source
    f.write(html)
