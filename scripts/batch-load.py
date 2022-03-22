#
"""
バッチ処理
"""

import os
import csv
import subprocess
import argparse
import logging

from nbformat import read

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

p = argparse.ArgumentParser()
p.add_argument('--input', default='dl-list.csv')
p.add_argument('--out', default='./downloads')
args = p.parse_args()

cmd = ['python3']

DOMAIN_GETUP = 'getuploader.com'

# getupload
cmd += ['scripts/dl-getup.py', '-n']

with open(args.input, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        iid, _, url, passwd = row
        if DOMAIN_GETUP in url:
            callcmd = cmd.copy()
            callcmd.append(url)
            outdir = f'{args.out}/{iid}'
            callcmd.append('-o')
            callcmd.append(outdir)
            if passwd != '':
                callcmd.append('-p')
                callcmd.append(passwd)
            logger.info(f'call cmd: {callcmd}')
            ret = subprocess.check_call(callcmd)
        
