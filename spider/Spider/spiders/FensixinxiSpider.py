# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import FensixinxiItem
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
# 粉丝信息
class FensixinxiSpider(scrapy.Spider):
    name = 'fensixinxiSpider'
    spiderUrl = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False


    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '7ph56346_fensixinxi') == 1:
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
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
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
            if self.table_exists(cursor, '7ph56346_fensixinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('ul#m-pl-container > li')
        for item in list:
            fields = FensixinxiItem()

            if '(.*?)' in '''a[class="tit f-thide s-fc0"]::text''':
                try:
                    fields["name"] = str( re.findall(r'''a[class="tit f-thide s-fc0"]::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["name"] = str( self.remove_html(item.css('''a[class="tit f-thide s-fc0"]::text''').extract_first()))

                except:
                    pass
            detailUrlRule = item.css('a[class="tit f-thide s-fc0"]::attr(href)').extract_first()
            detailUrlRule ='https://music.163.com'+ detailUrlRule 
            if self.protocol in detailUrlRule or detailUrlRule.startswith('http'):
                pass
            elif detailUrlRule.startswith('//'):
                detailUrlRule = self.protocol + ':' + detailUrlRule
            elif detailUrlRule.startswith('/'):
                detailUrlRule = self.protocol + '://' + self.hostname + detailUrlRule
            else:
                detailUrlRule = self.protocol + '://' + self.hostname + '/' + detailUrlRule
            yield scrapy.Request(url=detailUrlRule, meta={'fields': fields},  callback=self.detail_parse, dont_filter=True)

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        try:
            if '(.*?)' in '''a.f-tdn::attr(href)''':
                fields["fsdz"] = str('https://music.163.com/#'+ re.findall(r'''a.f-tdn::attr(href)''', response.text, re.S)[0].strip())

            else:
                if 'fsdz' != 'xiangqing' and 'fsdz' != 'detail' and 'fsdz' != 'pinglun' and 'fsdz' != 'zuofa':
                    fields["fsdz"] = str('https://music.163.com/#'+ self.remove_html(response.css('''a.f-tdn::attr(href)''').extract_first()))

                else:
                    try:
                        fields["fsdz"] = str('https://music.163.com/#'+ emoji.demojize(response.css('''a.f-tdn::attr(href)''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''a.f-tdn::attr(title)''':
                fields["fsmc"] = str( re.findall(r'''a.f-tdn::attr(title)''', response.text, re.S)[0].strip())

            else:
                if 'fsmc' != 'xiangqing' and 'fsmc' != 'detail' and 'fsmc' != 'pinglun' and 'fsmc' != 'zuofa':
                    fields["fsmc"] = str( self.remove_html(response.css('''a.f-tdn::attr(title)''').extract_first()))

                else:
                    try:
                        fields["fsmc"] = str( emoji.demojize(response.css('''a.f-tdn::attr(title)''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''a.f-tdn img::attr(src)''':
                fields["fstx"] = str( re.findall(r'''a.f-tdn img::attr(src)''', response.text, re.S)[0].strip())

            else:
                if 'fstx' != 'xiangqing' and 'fstx' != 'detail' and 'fstx' != 'pinglun' and 'fstx' != 'zuofa':
                    fields["fstx"] = str( self.remove_html(response.css('''a.f-tdn img::attr(src)''').extract_first()))

                else:
                    try:
                        fields["fstx"] = str( emoji.demojize(response.css('''a.f-tdn img::attr(src)''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''<span>所在地区：(.*?)</span>''':
                fields["szdq"] = str( re.findall(r'''<span>所在地区：(.*?)</span>''', response.text, re.S)[0].strip())

            else:
                if 'szdq' != 'xiangqing' and 'szdq' != 'detail' and 'szdq' != 'pinglun' and 'szdq' != 'zuofa':
                    fields["szdq"] = str( self.remove_html(response.css('''<span>所在地区：(.*?)</span>''').extract_first()))

                else:
                    try:
                        fields["szdq"] = str( emoji.demojize(response.css('''<span>所在地区：(.*?)</span>''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''个人介绍：(.*?)</div>''':
                fields["grjs"] = str( re.findall(r'''个人介绍：(.*?)</div>''', response.text, re.S)[0].strip())

            else:
                if 'grjs' != 'xiangqing' and 'grjs' != 'detail' and 'grjs' != 'pinglun' and 'grjs' != 'zuofa':
                    fields["grjs"] = str( self.remove_html(response.css('''个人介绍：(.*?)</div>''').extract_first()))

                else:
                    try:
                        fields["grjs"] = str( emoji.demojize(response.css('''个人介绍：(.*?)</div>''').extract_first()))

                    except:
                        pass
        except:
            pass
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider7ph56346?charset=UTF8MB4')
        df = pd.read_sql('select * from fensixinxi limit 50', con = engine)

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
            insert into `fensixinxi`(
                id
                ,name
                ,fsdz
                ,fsmc
                ,fstx
                ,szdq
                ,grjs
            )
            select
                id
                ,name
                ,fsdz
                ,fsmc
                ,fstx
                ,szdq
                ,grjs
            from `7ph56346_fensixinxi`
            where(not exists (select
                id
                ,name
                ,fsdz
                ,fsmc
                ,fstx
                ,szdq
                ,grjs
            from `fensixinxi` where
                `fensixinxi`.id=`7ph56346_fensixinxi`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
