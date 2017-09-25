#! /usr/bin/python
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import time

total_count = 300
item_per_page = 24
total_page = total_count / item_per_page + 1

item_urls = []
items = []

def get_url_from_one_page(page_url):
    wb_data = requests.get(page_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    urls = soup.select('a.resule_img_a')
    for url in urls:
        item_urls.append(url['href'])

def get_item_info(item_url):
    wb_data = requests.get(item_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.pho_info em')
    addresses = soup.select('div.pho_info > p > span.pr5')

    data = {
        'title': titles[0].get_text(),
        'address': addresses[0].get_text()
    }
    items.append(data)

urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,total_page + 1)]

for url in urls:
    time.sleep(2)
    get_url_from_one_page(url)

    for item_url in item_urls:
        get_item_info(item_url)
    item_urls = []

    for item in items:
        print item, '\n'




