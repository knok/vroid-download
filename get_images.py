# -*- coding: utf-8 -*-
#

import glob
import requests
import os
import time

from bs4 import BeautifulSoup

gpat = "seiga-html/maki/*.html"
files = glob.glob(gpat)


outdir = "seiga-thumb/maki"
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
