#! -*- coding:utf-8 -*-
import subprocess
import os
import threading
import time
import re
import sys
import json


## CONFIGS
with open('conf.json', 'r') as f:
    CONF = json.load(f)

BASE = CONF["BASE"]
ffmpeg = os.path.join(BASE, CONF["ffmpeg"])
youtube_dl = os.path.join(BASE, CONF["youtube_dl"])

def getUniqueFileName(filename, extension, outpath):
    index = 0
    while True:
        if f'{filename}-{index}.{outpath}' not in os.listdir(outpath):
            return f'{filename}-{index}.{extension}'
        else:
            index+=1

def download_live_stream(link, outpath, filename):
    global ffmpeg
    
    filename = getUniqueFileName(filename, 'ts', outpath)
    proc = subprocess.Popen([ffmpeg, '-i', link.replace('\n',''), '-c', 'copy', os.path.join(outpath, filename)])
    proc.communicate()

def download_video(link, outpath):
    proc = subprocess.Popen([youtube_dl, '--list-formats', link], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    formats = proc.communicate()[0].decode('cp1254')
    print(formats)
    format_code = input("Please enter the format code:")
    proc = subprocess.Popen([youtube_dl, '-f', format_code, "-o", r"downloads\%(title)s.%(ext)s",link])
    proc.communicate()
    
def resolve_link(link):
    resolve_link = subprocess.Popen([youtube_dl, '-f', 'best', '-g', link], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    link = resolve_link.communicate()[0].decode('utf-8')
    return link

    
if __name__ == '__main__':
    outpath = 'downloads'
    os.makedirs(outpath, exist_ok=True)
    
    #base_link = 'https://www.youtube.com/watch?v=GokkdRUQ3Ts'
    base_link = sys.argv[1]
    stream_link = resolve_link(base_link)
    is_live_stream = 'index' in os.path.basename(stream_link)

    print('Is live stream? :', is_live_stream)
    if is_live_stream:
        stream_name = input('Please enter the stream name:')
        th = threading.Thread(target=download_live_stream, args=(stream_link, outpath, stream_name))
        th.start()
        th.join()
    else:
        download_video(base_link, outpath)

