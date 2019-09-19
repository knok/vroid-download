# -*- coding: utf-8 -*-
#

import glob
import requests
import os
import time

from bs4 import BeautifulSoup

urls = {
  "yukari": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%B5%90%E6%9C%88%E3%82%86%E3%81%8B%E3%82%8A",
  "maki": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E5%BC%A6%E5%B7%BB%E3%83%9E%E3%82%AD",
  "zunko": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%81%9A%E3%82%93%E5%AD%90",
  "kotonoha": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%90%B4%E8%91%89%E8%8C%9C%E3%83%BB%E8%91%B5",
  "kiri": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%81%8D%E3%82%8A%E3%81%9F%E3%82%93",
  "itako": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E6%9D%B1%E5%8C%97%E3%82%A4%E3%82%BF%E3%82%B3",
  "akari": "https://wikiwiki.jp/voirosozai/%E7%AB%8B%E3%81%A1%E7%B5%B5%EF%BC%8F%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/%E7%B4%B2%E6%98%9F%E3%81%82%E3%81%8B%E3%82%8A"
}

def get_char_images(cname):
    gpat = "seiga-html/%s/*.html" % cname
    files = glob.glob(gpat)

    outdir = "seiga-thumb/" + cname
    os.makedirs(outdir, exist_ok=True)
    for fname in files:
        x = os.path.basename(fname)
        imname, _ = os.path.splitext(x)
        out_imagefname = "%s/%s.jpg" % (outdir, imname)
        with open(fname) as f:
            html = f.read()
        bs = BeautifulSoup(html, 'lxml')
        try:
            elem = bs.select('#link_thumbnail_main img')[0]
            url = elem.get('src')
            r = requests.get(url, stream=True)
            with open(out_imagefname, 'wb') as f:
                f.write(r.content)
        except:
            pass
        print(out_imagefname, url)
        time.sleep(1)

def main():
    global urls
    for cname in urls.keys():
        get_char_images(cname)

if __name__ == "__main__":
  main()
