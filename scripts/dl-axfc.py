#
"""
axfc.net からダウンロードを行う
"""

import os
import sys
import argparse
import time
import logging
import subprocess

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

p = argparse.ArgumentParser()
p.add_argument('url')
p.add_argument('--password', '-p', default='')
p.add_argument('--output-dir', '-o', default='out')
p.add_argument('--no-headless', '-n', default=False, action='store_true')
args = p.parse_args()

dldir = os.path.abspath(args.output_dir)
# ref: https://www.browserstack.com/guide/download-file-using-selenium-python
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", dldir)
#Example:profile.set_preference("browser.download.dir", "C:\Tutorial\down")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

options = Options()
if not args.no_headless:
  options.add_argument('--headless')

driver:WebDriver = webdriver.Firefox(firefox_profile=profile, options=options)

url = args.url
if url.find('?key=') < 0:
    # keyをもっていない場合
    if args.password != '':
        url += f'?key={args.password}'
    else:
        # パスワード情報なし
        pass

driver.get(url)

# キーワードチェック
try:
    keyword = driver.find_element_by_css_selector('input[name="keyword"]')
except NoSuchElementException as e:
    logger.error(f'no keyword input element: {e}')
    driver.close()
    sys.exit(0)

if url.find('?key=') < 0:
    keyword.send_keys(args.password)

# ボタンのチェック
try:
    button = driver.find_element_by_css_selector('input.button')
except NoSuchElementException as e:
        logger.error(f'no input button: {e}')
        driver.close()
        sys.exit(0)

# ダウンロードページ遷移
button.click()
time.sleep(5)

anchors = driver.find_elements_by_css_selector('a')
for target in anchors:
    if target.text.find('ダウンロードする') > 0:
        break
os.makedirs(dldir, exist_ok=True)
# bad page
if target.text.find('ダウンロードする') < 0:
    logger.error(f'bad page: pass:{args.password}')
    driver.close()
    sys.exit(0)

# ダウンロード開始
target.click()
time.sleep(5)

anchors = driver.find_elements_by_css_selector('a')
for target in anchors:
    if target.text.find('こちら') >= 0:
        break
# bad page:
if target.text.find('こちら') < 0:
    logger.error(f'bad page: pass:{args.password}')
    driver.close()
    sys.exit(0)
# 強制ダウンロード
# target.click()
link = target.get_attribute('href')
os.chdir(dldir)
subprocess.check_call(['wget', '--no-check-certificate', link])

time.sleep(5)

driver.close()
