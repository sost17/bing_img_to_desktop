# coding = utf-8

import os
import win32api
import win32gui

import requests
import win32con
from lxml import etree


class DownloadBingImg:
    def __init__(self, url):
        self.image_name = r'C:\Users\Public\desktopimage.jpg'
        if os.path.exists(self.image_name):
            os.remove(self.image_name)
            print('图片删除成功')
        self.file = ''
        self.base_url = url
        self.headers = {
            "authority": "cn.bing.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"104\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"14.0.0\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
            "x-client-data": "eyIyIjoiMCIsIjMiOiIwIiwiNCI6Ii01MDEzNDI2OTQzNjM2NTM1MTk4IiwiNSI6IlwiUUVoRmN5OVRpRlJManpRajhDWHllWUZzVUY3SUxHZEdGUWREOFVoN3NzVT1cIiIsIjYiOiJzdGFibGUiLCI3IjoiNjA1NTkwMzg4NzM3IiwiOSI6ImRlc2t0b3AifQ==",
            "x-edge-shopping-flag": "1"
        }

    def get_bing_img(self):
        req = requests.get(self.base_url, headers=self.headers)
        selector = etree.HTML(req.text)
        link = selector.xpath('//link[@id="preloadBg"]/@href')
        if link:
            img_url = link[0]
            print('找到Bing壁纸')
            return img_url
        return None

    def download_image_file(self, url):
        img_req = requests.request(method='GET', url=url, stream='true').content

        with open(self.image_name, 'wb') as wfile:
            wfile.write(img_req)
        print('图片下载成功')

    def change_desktop_image(self):
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.image_name, 1 + 2)
        print('桌面壁纸设置成功')

    def main(self):
        img_url = self.get_bing_img()
        if img_url:
            if 'https://' not in img_url:
                img_url = self.base_url + img_url
            self.download_image_file(img_url)
            self.change_desktop_image()


if __name__ == '__main__':
    gbi = DownloadBingImg('https://cn.bing.com/')
    gbi.main()
