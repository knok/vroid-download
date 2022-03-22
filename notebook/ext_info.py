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
pass_pat = re.compile('(?:PASS|パス)(?:ワード|word)?[:：= ]*(?:[\sは＝⇒・ ])*[\[(「【]?([^]」】\n)　]*)[\]())で」】]?', re.MULTILINE | re.IGNORECASE)
pass_pat_nl = re.compile('(?:PASS|パス)(?:ワード|word)?.*\n\s*[\[(「【]?([^]」】\n]*)[\])」】]?', re.MULTILINE| re.IGNORECASE)

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

def get_password(text):
    # if 'パス' in text or 'pass' in text.lower():
    #     logger.info(f'contains pass: {text}')
    match = pass_pat.search(text)
    if not match is None:
        cand = match.group(1)
        if cand != '':
            return cand # 発見パスワード
    match = pass_pat_nl.search(text)
    if match is None:
        return ''
    return match.group(1)

def ext_info(text):
    passwd =  get_password(text)
    match = urlpat.findall(text)
    if len(match) == 0:
        match = ''
    else:
        match = match[0]
    return match, passwd

def main():
    args = get_args()
    files = get_files(args.file_pat)
    for file in tqdm.tqdm(files):
        # logger.info(file)
        origurl = fname2url(file)
        text = ext_description(file)
        # print(text)
        url, passwd = ext_info(text)
        # print(match)
        # logger.info(f'URL:{url}, pass:{passwd}')
        print(f'page:{origurl}, download:{url}, pass:{passwd}')

if __name__ == '__main__':
    main()
