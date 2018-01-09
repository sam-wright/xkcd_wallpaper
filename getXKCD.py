#!/usr/bin/python3


import textwrap
import os
import json
from urllib.request import Request, urlopen
from urllib.error import  URLError
from PIL import Image, ImageFont, ImageDraw


def safe_request(url):
    """
    """

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

def title2image(text):
    """
    """

    font = ImageFont.truetype('Humor-Sans.ttf', 25)
    textW, textH = font.getsize("S")
    xkcd = Image.open('image.png')
    xwidth, xheight = xkcd.size
    img = Image.new("RGBA", (xwidth, 588), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    margin = offset = 4
    for line in textwrap.wrap(text, width=xwidth/textW-1):
        draw.text((margin, offset), line, font=font, fill=(0, 0, 0))
        offset += font.getsize(line)[1]
        img = img.crop((0, 0, xwidth, offset+textH))
    return img

def alt2image(alt_text):
    """
    """

    font = ImageFont.truetype('Humor-Sans.ttf', 14)
    textW, textH = font.getsize("S")
    xkcd = Image.open('image.png')
    xwidth, xheight = xkcd.size
    img = Image.new("RGBA", (xwidth, 588), (190, 190, 190))
    draw = ImageDraw.Draw(img)
    margin = offset = 5
    for line in textwrap.wrap(alt_text, width=xwidth/textW-6):
        draw.text((margin, offset), line, font=font, fill=(0, 0, 0))
        offset += font.getsize(line)[1]
    img = img.crop((0, 0, xwidth, offset + textH))
    return img

def stitchImagesTogether(headerImg, textImg):
    """
    """

    sideMargin = 20
    xImg = Image.open('image.png')
    xw, xh = xImg.size
    tw, th = textImg.size
    hw, hh = headerImg.size
    xImg_mouseover_space = 8
    img = Image.new("RGBA", (xw+sideMargin*2, xh + th + hh + 2*sideMargin + \
                    xImg_mouseover_space), (255, 255, 255))
    img.paste(headerImg, (sideMargin, sideMargin))
    img.paste(xImg, (sideMargin, hh + sideMargin))
    img.paste(textImg, (sideMargin, sideMargin + xh + hh + \
              xImg_mouseover_space))
    img.save('wallpaper.png')

def get_today():
    """
    """

    page = safe_request('https://xkcd.com/info.0.json')
    data = json.load(page)

    alt = data['alt']
    title = data['title']
    img_url = data['img']

    img = safe_request(img_url)
    with open('image.png', 'wb') as f:
        f.write(img.read())

    title_img = title2image(title)
    alt_img = alt2image(alt)

    stitchImagesTogether(title_img, alt_img)

    osString = 'gsettings set org.gnome.desktop.background picture-uri file://'\
             + os.getcwd() + '/wallpaper.png'
    os.system(osString)
    osString = 'gsettings set org.gnome.desktop.background picture-options centered'
    os.system(osString)

if __name__ == '__main__':
    get_today()
