#!/usr/bin/python3

from urllib.request import Request, urlopen
from urllib.error import  URLError
import json

def safe_request(url):
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        # everything is fine
        return response

page = safe_request('https://xkcd.com/info.0.json')
data = json.load(page)

alt = data['alt']
title = data['title']
img_url = data['img']

img = safe_request(img_url)
with open('image.png', 'wb') as f:
    f.write(img.read())
