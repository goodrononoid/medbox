#-*- coding:utf-8 -*-
#!python

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib

medurl = 'https://medbox.ru/2016/'

# standart headers
headers_standart = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding' : 'gzip,deflate,sdch',
           'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
           'Cache-Control' : 'max-age=0'}

data = {}
data['nextButton'] = urllib.parse.quote('Продолжить')
data['citylist'] = urllib.parse.quote('Нижневартовск')

s = requests.Session()
s.headers.update(headers_standart) # может это лишнее ?
r = s.get(medurl)
print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), s.cookies.get_dict(), '\n')

# make new header 'Set-Cookie'
session_id = r.headers['Set-Cookie'][18:42]

s.headers['Set-Cookie'] = 'ASP.NET_SessionId=' + session_id + '; path=/; HttpOnly, __Region={"End":3000518655,"Region":"86","Name":"' + data['citylist'] + '"}; path=/; _ym_uid=1511438481466314529; _ga=GA1.2.1754532188.1511438481; _gid=GA1.2.418642800.1511438481; _ym_visorc_41304969=w; _ym_isad=2; _ym_visorc_27732045=w'

cookies_chrome = {
	'_ga' : 'GA1.2.1083857719.1509363136',
	'_ym_uid' : '1509363136916671318',
	'__Region' : '%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D'
}
requests.cookies.remove_cookie_by_name(s.cookies, '__Region')
requests.cookies.merge_cookies(s.cookies, cookies_chrome)

r.headers['Set-Cookie'] = 'ASP.NET_SessionId=sogtxqjljuyfg25xaq5nlbc3; path=/; HttpOnly, __Region=%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D; path=/; _ym_uid=1509363136916671318; path=/; _ga=GA1.2.1083857719.1509363136; path=/'

# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())
#
# # 
# region = soup.find('select', id = 'region_selector')
# print(region.prettify())
# city = soup.find('span', id = 'hmao_town_list')
# nv86 = city.find('option', value = 'Нижневартовск')
# print(nv86)

r2 = s.post(url=medurl, data=data, headers = {'Referer': r.url})

#r2 = s.post(url=medurl, data=data, cookies = s.cookies, headers = s.headers)
print('r2:\n URL:', r2.url, r2.history, '\n', 'Status:', r2, '\n', 'Cookies:', r2.cookies.get_dict(), s.cookies.get_dict(), '\n')

r3 = s.get('https://medbox.ru/2016/Rec/SelectDept', headers = {'Referer': r2.url})
print('r3:\n URL:', r3.url, r3.history, '\n', 'Status:', r3, '\n', 'Cookies:', r3.cookies, s.cookies.get_dict(), '\n')
