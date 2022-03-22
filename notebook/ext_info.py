#
"""
保存したHTMLからの情報抽出
"""

import os
import re
import glob
import argparse
import logging
import dbm

import tqdm
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

db = dbm.open('seiga-info.db', 'c')
urlpat = re.compile('https?://[\w!?/+\-_~=;.,*&@#$%()\'[\]]+')

def get_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument('--file-pat', default='seiga-html/*/*.html')
    args = p.parse_args()
    return args

def get_files(pattern):
    files = glob.glob(pattern)
    return files

def fname2url(fname):
    basename = os.path.splitext(os.path.basename(fname))[0]
    return f'https://seiga.nicovideo.jp/seiga/{basename}'

def ext_description(fname):
    with open(fname) as f:
        html = f.read()
    soup = BeautifulSoup(html)
    divs = soup.find_all('p',class_='discription')
    if len(divs) == 0:
        return ''
    return divs[0].text

def ext_info(text):
    match = urlpat.findall(text)
    return match

def main():
    args = get_args()
    files = get_files(args.file_pat)
    for file in tqdm.tqdm(files):
        # logger.info(file)
        url = fname2url(file)
        text = ext_description(file)
        # print(text)
        match = ext_info(text)
        print(match)
        logger.info(url)

if __name__ == '__main__':
    main()
