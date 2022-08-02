# -*- coding: utf-8 -*-
#
import argparse
import urllib
import re
import os
import time
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
import requests

logger = logging.getLogger(__name__)

p = argparse.ArgumentParser()
p.add_argument('--save-dir', default='vroid-images')
p.add_argument('--account', '-a', default='')
p.add_argument('--password', '-p', default='')
p.add_argument('--no-headless', '-n', default=False, action='store_true')
args = p.parse_args()

os.makedirs(args.save_dir, exist_ok=True)

acct = os.environ.get('NICO_ACCT', '')
if acct == '':
  acct = args.account
password = os.environ.get('NICO_PASSWD', '')
if password == '':
  password = args.password

def login_nico(driver:WebDriver):
  driver.get('https://account.nicovideo.jp/login')
  inp = driver.find_element_by_id('input__mailtel')
  inp.send_keys(acct)
  inp = driver.find_element_by_id('input__password')
  inp.send_keys(password)
  inp = driver.find_element_by_id('login__submit')
  inp.click()

options = Options()
if not args.no_headless:
  options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=options)

login_nico(driver)

start_url = 'https://seiga.nicovideo.jp/search/voiceroid?target=illust_all&sort=&sort=image_view'
pages_url = 'https://seiga.nicovideo.jp/search/voiceroid?&target=illust_all&sort=image_view&page='


def get_urls(url):
  """
  検索ページから個別画像へのリンクを集める
  """
  driver.get(url)

  # seigaのURLだけ集める
  urls_seiga = []
  for elem in driver.find_elements_by_css_selector('.thumb_title a'):
    url = elem.get_attribute('href')
    #import pdb; pdb.set_trace()
    if url.startswith('https://seiga.nicovideo.jp/seiga/im'): # user情報は除く
      if url.find('?') > 0:
        url = url[:url.find('?')] # パラメータの削除
      urls_seiga.append(url)
    elif url.startswith('/seiga'):
      if url.find('?') > 0:
        url = url[:url.find('?')] # パラメータの削除
      surl = f'https://seiga.nicovideo.jp{url}'
      urls_seiga.append(surl)
  return urls_seiga

def seigaid(url):
  id = re.sub('https://seiga.nicovideo.jp/seiga/', '', url)
  return id

# https://gist.github.com/morita-it-lab/3d50ec0ee4e0cc5f6f6d62b23720643f
def save_binary(url, filepath):
    js = """
    var getBinaryResourceText = function(url) {
        var req = new XMLHttpRequest();
        req.open('GET', url, false);
        req.overrideMimeType('text/plain; charset=x-user-defined');
        req.send(null);
        if (req.status != 200) return '';

        var filestream = req.responseText;
        var bytes = [];
        for (var i = 0; i < filestream.length; i++){
            bytes[i] = filestream.charCodeAt(i) & 0xff;
        }

        return bytes;
    }
    """
    js += "return getBinaryResourceText(\"{url}\");".format(url=url)

    data_bytes = driver.execute_script(js)
    with open(filepath, 'wb') as bin_out:
        bin_out.write(bytes(data_bytes))

def get_image(save_dir, url):
  driver.get(url)
  image_elem = driver.find_element_by_css_selector('#illust_link')
  img_view_url = image_elem.get_attribute('href') # like https://seiga.nicovideo.jp/image/source/5744216
  driver.get(img_view_url)
  elem = driver.find_element_by_css_selector('.illust_view_big img')
  img_url = elem.get_attribute('src')
  img_fname = img_url.split('/')[-1]
  out_imgfname = os.path.join(save_dir, img_fname)
  save_binary(img_url, out_imgfname)

def retry_get(url, wait=1, retry=3):
  for i in range(retry):
    driver.get(url)
    html = driver.page_source
    time.sleep(wait)
    if "Http/1.1 Service Unavailable" in html:
      continue
    print(url)
    return html
  return ""
  

def main():
  global urls
  
  urls = get_urls(start_url)
  # print(urls)
  for url in urls:
    get_image(args.save_dir, url)

if __name__ == "__main__":
  main()
