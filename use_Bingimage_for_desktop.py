# coding = utf-8

import os
import win32api
import win32con
import win32gui
import requests
from lxml import etree

baseurl = 'http://www.bing.com'
imagename = r'C:/Users/Public/desktopimage.jpg'
file = ''


def get_bingimg(url):
    req = requests.get(url)
    selector = etree.HTML(req.text)
    Link = selector.xpath('//link[@id="preloadBg"]/@href')
    if Link:
        img_url = Link[0]
        print('找到Bing壁纸')
        downloadimagefile(img_url)


def downloadimagefile(url):
    img_req = requests.request(method='GET', url=url, stream='true').content

    if os.path.exists(imagename):
        os.remove(imagename)
        print('图片删除成功')

    with open(imagename, 'wb') as wfile:
        wfile.write(img_req)
    print('图片下载成功')


def changedesktopimage():
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagename, 1 + 2)
    print('桌面壁纸设置成功')


if __name__ == '__main__':
    get_bingimg(baseurl)
    changedesktopimage()
