# -*- coding: utf-8 -*-
#

import glob
import os

import cv2

jpg_pat = 'seiga-thumb/*/*.jpg'
files = glob.glob(jpg_pat)
cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")

def detect_save(fname, outbase):
    image = cv2.imread(fname, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
    for i, (x, y, w, h) in enumerate(faces):
        print(x, y, w, h)
        ofname = "%s_%d.png" % (outbase, i)
        rimg = image[y:y+h, x:x+w]
        cv2.imwrite(ofname, rimg)
    return

# 逐次処理して結果を出力
outdir = 'faces'
for fname in files:
    imgidm, _ = os.path.splitext(os.path.basename(fname))
    basename = os.path.basename(fname)
    outfname = os.path.join(outdir, basename)
    detect_save(fname, outfname)
