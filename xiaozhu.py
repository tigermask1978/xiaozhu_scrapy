#! /usr/bin/python
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import pymongo
import time

total_count = 300
item_per_page = 24
total_page = total_count / item_per_page + 1

item_urls = []
items = []

#设置MongoDB
client = pymongo.MongoClient('localhost', 27017)
DB = client['XiaoZhu']
table = DB['page_info']

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

#获取一页信息并存入MongoDB
def get_info_of_one_page(page_url):
    time.sleep(2)
    wb_data = requests.get(page_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    addresses = soup.select('span.result_title')
    prices = soup.select('span.result_price > i')
    for address, price in zip(addresses, prices):
        table.insert_one({
            'address': address.get_text(),
            'price': int(price.get_text())
        })


if __name__ == '__main__':
    '''
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,total_page + 1)]
    for url in urls:
        time.sleep(2)
        get_url_from_one_page(url)

        for item_url in item_urls:
            get_item_info(item_url)
        item_urls = []

        for item in items:
            print item, '\n'
    '''
    #获取3页数据
    # urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1, 4)]
    # for url in urls:
    #     get_info_of_one_page(url)
    # print 'Write Data Done!'

    #查找价格大于等于500元的房源
    for item in table.find({'price': {'$gte': 500}}):
        print item, '\n'




