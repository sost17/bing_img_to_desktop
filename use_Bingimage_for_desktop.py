#coding = utf-8

import os
import win32api
import win32con
import win32gui
import requests
from bs4 import BeautifulSoup

baseurl ='http://www.bing.com'
imagename = r'C:/Users/Public/desktopimage.jpg'
file = ''

def get_bingimg(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    Link = soup.find_all(id="bgLink")
    for href in Link:
        print('找到Bing壁纸')
        downloadimagefile(baseurl + href.get('href'))
    

def downloadimagefile(url):
    img_req=requests.request(method='GET',url=url,stream='true').content
    file = open(imagename,'wb')
    file.write(img_req)
    file.close()
    print('图片下载成功')

def changedesktopimage():
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key,"WallpaperStyle",0,win32con.REG_SZ,"2")
    win32api.RegSetValueEx(key,"TileWallpaper",0,win32con.REG_SZ,"0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagename,1+2)
    print('桌面壁纸设置成功')
    os.remove(imagename)
    print('图片删除成功')

if __name__ == '__main__':
    get_bingimg(baseurl)
    changedesktopimage()
