# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython


#%%
import glob
import os

import cv2
from PIL import Image
import numpy as np


#%%
jpg_pat = 'seiga-thumb/*.jpg'
files = glob.glob(jpg_pat)


#%%
cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")


#%%
def detect(fname):
    image = cv2.imread(fname, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)# , minsize=(24, 24))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    rgb_cv = image[:, :, ::-1].copy()
    img = Image.fromarray(rgb_cv)
    return img


#%%
# 逐次処理して結果を出力
get_ipython().system(' mkdir -p tmp')
outdir = 'tmp'
for fname in files:
    basename = os.path.basename(fname)
    outfname = os.path.join(outdir, basename)
    img = detect(fname)
    img.save(outfname)


#%%



