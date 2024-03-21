import time

import requests
import re
from lib.request.headers import create_headers
from bs4 import BeautifulSoup

city ='tangshan'
area = ''
datas = []
for year in range(2011,2025):
    time.sleep(5)
    url = 'https://www.anjuke.com/fangjia/{0}{1}/{2}'.format(city,year,area)
    headers = create_headers()
    response = requests.get(url, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    year_section = soup.find_all('section',class_ = 'ranklist')[0]
    month_sections = year_section.find_all('div',class_ = 'table is-headless')[0].find_all('div',class_ ='table-tr')
    for month_section in month_sections:
        date = month_section.find_all('div',class_ ='td')[0].text.strip()
        price = month_section.find_all('div',class_ ='td')[1].text.strip()
        print(date,"#",price)
        datas.append(date+','+price)

csv_file = "data/history/{0}.csv".format(city)
with open(csv_file, "a+",encoding='utf-8') as f:
    # 开始获得需要的板块数据
    total_num = len(datas)
    for data in datas:
        f.write(data + "\n")