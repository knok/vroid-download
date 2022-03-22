#
"""
getuploader.com からダウンロードを行う
"""

import os
import argparse
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

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

driver.get(args.url)

elem = driver.find_element_by_name('password')
if elem is not None:
    elem.send_keys(args.password)

elem = driver.find_elements_by_css_selector('button.is_black')
if len(elem) > 0:
    elem[0].click()

elem = driver.find_elements_by_css_selector('input.btn.btn-default')


os.makedirs(dldir, exist_ok=True)
elem[0].click()
time.sleep(10)

elem = driver.find_elements_by_css_selector('button.is_black')
if len(elem) > 0:
    elem[0].click()

elem = driver.find_elements_by_css_selector('input.btn.btn-default')
elem[0].click()

time.sleep(30)

driver.close()
