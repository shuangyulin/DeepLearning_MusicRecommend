# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import GedaninfoItem
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
# 歌单信息
class GedaninfoSpider(scrapy.Spider):
    name = 'gedaninfoSpider'
    spiderUrl = 'https://music.163.com/weapi/user/playlist?csrf_token=ba02701d02ad8cfe8bc89ed06c284221'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False

    headers = {
        'Cookie':''
    }

    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '7ph56346_gedaninfo') == 1:
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
            if self.table_exists(cursor, '7ph56346_gedaninfo') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        data = json.loads(response.body)
        try:
            list = data["playlist"]
        except:
            pass
        for item in list:
            fields = GedaninfoItem()


            try:
                fields["gdname"] = emoji.demojize(self.remove_html(str( item["name"] )))

            except:
                pass
            try:
                fields["imgurl"] = emoji.demojize(self.remove_html(str( item["coverImgUrl"] )))

            except:
                pass
            try:
                fields["description"] = emoji.demojize(self.remove_html(str( item["description"] )))

            except:
                pass
            try:
                fields["gdid"] = emoji.demojize(self.remove_html(str( item["id"] )))

            except:
                pass
            try:
                fields["playcount"] = int( item["playCount"])
            except:
                pass
            try:
                fields["subscribedcount"] = int( item["subscribedCount"])
            except:
                pass
            try:
                fields["cjtime"] = emoji.demojize(self.remove_html(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( item["createTime"]/1000)) )))

            except:
                pass
            try:
                fields["detailurl"] = emoji.demojize(self.remove_html(str('https://music.163.com/#/playlist?id='+str( item["id"]) )))

            except:
                pass
            yield fields

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider7ph56346?charset=UTF8MB4')
        df = pd.read_sql('select * from gedaninfo limit 50', con = engine)

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
            insert into `gedaninfo`(
                id
                ,gdname
                ,imgurl
                ,description
                ,gdid
                ,playcount
                ,subscribedcount
                ,cjtime
                ,detailurl
            )
            select
                id
                ,gdname
                ,imgurl
                ,description
                ,gdid
                ,playcount
                ,subscribedcount
                ,cjtime
                ,detailurl
            from `7ph56346_gedaninfo`
            where(not exists (select
                id
                ,gdname
                ,imgurl
                ,description
                ,gdid
                ,playcount
                ,subscribedcount
                ,cjtime
                ,detailurl
            from `gedaninfo` where
                `gedaninfo`.id=`7ph56346_gedaninfo`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
