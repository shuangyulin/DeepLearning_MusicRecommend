# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import SonginfoItem
import time
from datetime import datetime,timedelta
import datetime as formattime
import re
import random
import platform
import json
import os
import urllib
from urllib.parse import urlparse
import requests
import emoji
import numpy as np
from DrissionPage import Chromium
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 歌曲信息
class SonginfoSpider(scrapy.Spider):
    name = 'songinfoSpider'
    spiderUrl = 'https://music.163.com/#/playlist?id=2235360369'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False

    headers = {
        'Cookie': ''
    }

    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '7ph56346_songinfo') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        pageNum = 1 + 1

        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):

                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        headers=self.headers,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '7ph56346_songinfo') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('table[class="m-table "] tbody tr')
        for item in list:
            fields = SonginfoItem()
            if '(.*?)' in '''td:nth-child(2) b::attr(title)''':
                try:
                    fields["songtitle"] = str( re.findall(r'''td:nth-child(2) b::attr(title)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["songtitle"] = str( self.remove_html(item.css('''td:nth-child(2) b::attr(title)''').extract_first()))

                except:
                    pass

            if '(.*?)' in '''td:nth-child(3) span[class="u-dur "]::text''':
                try:
                    fields["shichang"] = str( re.findall(r'''td:nth-child(3) span[class="u-dur "]::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["shichang"] = str( self.remove_html(item.css('''td:nth-child(3) span[class="u-dur "]::text''').extract_first()))

                except:
                    pass

            if '(.*?)' in '''td:nth-child(4) div.text::attr(title)''':
                try:
                    fields["singer"] = str( re.findall(r'''td:nth-child(4) div.text::attr(title)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["singer"] = str( self.remove_html(item.css('''td:nth-child(4) div.text::attr(title)''').extract_first()))

                except:
                    pass

            if '(.*?)' in '''td:nth-child(5) a::attr(title)''':
                try:
                    fields["zhuanji"] = str( re.findall(r'''td:nth-child(5) a::attr(title)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["zhuanji"] = str( self.remove_html(item.css('''td:nth-child(5) a::attr(title)''').extract_first()))

                except:
                    pass

            if '(.*?)' in '''div#song-list-pre-cache::attr(data-key)''':
                try:
                    fields["gdid"] = str( re.findall(r'''div#song-list-pre-cache::attr(data-key)''', item.extract(), re.DOTALL)[0].strip().replace('track_playlist-',''))

                except:
                    pass
            else:
                try:
                    fields["gdid"] = str( self.remove_html(item.css('''div#song-list-pre-cache::attr(data-key)''').extract_first()).replace('track_playlist-',''))

                except:
                    pass

            if '(.*?)' in '''td:nth-child(2) a::attr(href)''':
                try:
                    fields["detailurl"] = str('https://music.163.com/#'+ re.findall(r'''td:nth-child(2) a::attr(href)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["detailurl"] = str('https://music.163.com/#'+ self.remove_html(item.css('''td:nth-child(2) a::attr(href)''').extract_first()))

                except:
                    pass

            yield fields


    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider7ph56346?charset=UTF8MB4')
        df = pd.read_sql('select * from songinfo limit 50', con = engine)

        # 重复数据过滤
        df.duplicated()
        df.drop_duplicates()

        #空数据过滤
        df.isnull()
        df.dropna()

        # 填充空数据
        df.fillna(value = '暂无')

        # 异常值过滤

        # 滤出 大于800 和 小于 100 的
        a = np.random.randint(0, 1000, size = 200)
        cond = (a<=800) & (a>=100)
        a[cond]

        # 过滤正态分布的异常值
        b = np.random.randn(100000)
        # 3σ过滤异常值，σ即是标准差
        cond = np.abs(b) > 3 * 1
        b[cond]

        # 正态分布数据
        df2 = pd.DataFrame(data = np.random.randn(10000,3))
        # 3σ过滤异常值，σ即是标准差
        cond = (df2 > 3*df2.std()).any(axis = 1)
        # 不满⾜条件的⾏索引
        index = df2[cond].index
        # 根据⾏索引，进⾏数据删除
        df2.drop(labels=index,axis = 0)

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8mb4')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `songinfo`(
                id
                ,songtitle
                ,shichang
                ,singer
                ,zhuanji
                ,gdid
                ,detailurl
            )
            select
                id
                ,songtitle
                ,shichang
                ,singer
                ,zhuanji
                ,gdid
                ,detailurl
            from `7ph56346_songinfo`
            where(not exists (select
                id
                ,songtitle
                ,shichang
                ,singer
                ,zhuanji
                ,gdid
                ,detailurl
            from `songinfo` where
                `songinfo`.id=`7ph56346_songinfo`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
