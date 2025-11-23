# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import GequxinxiItem
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
class GequxinxiSpider(scrapy.Spider):
    name = 'gequxinxiSpider'
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
            if self.table_exists(cursor, '7ph56346_gequxinxi') == 1:
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
            if self.table_exists(cursor, '7ph56346_gequxinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('ul#m-pl-container > li')
        for item in list:
            fields = GequxinxiItem()

            if '(.*?)' in '''a[class="tit f-thide s-fc0"]::text''':
                try:
                    fields["title"] = str( re.findall(r'''a[class="tit f-thide s-fc0"]::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["title"] = str( self.remove_html(item.css('''a[class="tit f-thide s-fc0"]::text''').extract_first()))

                except:
                    pass
            if '(.*?)' in '''img.j-flag::attr(src)''':
                try:
                    fields["picture"] = str( re.findall(r'''img.j-flag::attr(src)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["picture"] = str( self.remove_html(item.css('''img.j-flag::attr(src)''').extract_first()))

                except:
                    pass
            if '(.*?)' in '''a[class="nm nm-icn f-thide s-fc3"]::text''':
                try:
                    fields["zuozhe"] = str( re.findall(r'''a[class="nm nm-icn f-thide s-fc3"]::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["zuozhe"] = str( self.remove_html(item.css('''a[class="nm nm-icn f-thide s-fc3"]::text''').extract_first()))

                except:
                    pass
            if '(.*?)' in '''a[class="tit f-thide s-fc0"]::attr(href)''':
                try:
                    fields["xqdz"] = str('https://music.163.com'+ re.findall(r'''a[class="tit f-thide s-fc0"]::attr(href)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["xqdz"] = str('https://music.163.com'+ self.remove_html(item.css('''a[class="tit f-thide s-fc0"]::attr(href)''').extract_first()))

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
            if '(.*?)' in '''a[class="u-btni u-btni-fav "]::attr(data-count)''':
                fields["shoucang"] = int( re.findall(r'''a[class="u-btni u-btni-fav "]::attr(data-count)''', response.text, re.S)[0].strip())
            else:
                if 'shoucang' != 'xiangqing' and 'shoucang' != 'detail' and 'shoucang' != 'pinglun' and 'shoucang' != 'zuofa':
                    fields["shoucang"] = int( self.remove_html(response.css('''a[class="u-btni u-btni-fav "]::attr(data-count)''').extract_first()))
                else:
                    try:
                        fields["shoucang"] = int( emoji.demojize(response.css('''a[class="u-btni u-btni-fav "]::attr(data-count)''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''a[class="u-btni u-btni-share "]::attr(data-count)''':
                fields["share"] = int( re.findall(r'''a[class="u-btni u-btni-share "]::attr(data-count)''', response.text, re.S)[0].strip())
            else:
                if 'share' != 'xiangqing' and 'share' != 'detail' and 'share' != 'pinglun' and 'share' != 'zuofa':
                    fields["share"] = int( self.remove_html(response.css('''a[class="u-btni u-btni-share "]::attr(data-count)''').extract_first()))
                else:
                    try:
                        fields["share"] = int( emoji.demojize(response.css('''a[class="u-btni u-btni-share "]::attr(data-count)''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''span#cnt_comment_count::text''':
                fields["pinglun"] = int( re.findall(r'''span#cnt_comment_count::text''', response.text, re.S)[0].strip())
            else:
                if 'pinglun' != 'xiangqing' and 'pinglun' != 'detail' and 'pinglun' != 'pinglun' and 'pinglun' != 'zuofa':
                    fields["pinglun"] = int( self.remove_html(response.css('''span#cnt_comment_count::text''').extract_first()))
                else:
                    try:
                        fields["pinglun"] = int( emoji.demojize(response.css('''span#cnt_comment_count::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''strong#play-count::text''':
                fields["bofang"] = int( re.findall(r'''strong#play-count::text''', response.text, re.S)[0].strip())
            else:
                if 'bofang' != 'xiangqing' and 'bofang' != 'detail' and 'bofang' != 'pinglun' and 'bofang' != 'zuofa':
                    fields["bofang"] = int( self.remove_html(response.css('''strong#play-count::text''').extract_first()))
                else:
                    try:
                        fields["bofang"] = int( emoji.demojize(response.css('''strong#play-count::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''p#album-desc-more''':
                fields["jieshao"] = str( re.findall(r'''p#album-desc-more''', response.text, re.S)[0].strip())

            else:
                if 'jieshao' != 'xiangqing' and 'jieshao' != 'detail' and 'jieshao' != 'pinglun' and 'jieshao' != 'zuofa':
                    fields["jieshao"] = str( self.remove_html(response.css('''p#album-desc-more''').extract_first()))

                else:
                    try:
                        fields["jieshao"] = str( emoji.demojize(response.css('''p#album-desc-more''').extract_first()))

                    except:
                        pass
        except:
            pass
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider7ph56346?charset=UTF8MB4')
        df = pd.read_sql('select * from gequxinxi limit 50', con = engine)

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
            insert into `gequxinxi`(
                id
                ,title
                ,picture
                ,zuozhe
                ,xqdz
                ,shoucang
                ,share
                ,pinglun
                ,bofang
                ,jieshao
            )
            select
                id
                ,title
                ,picture
                ,zuozhe
                ,xqdz
                ,shoucang
                ,share
                ,pinglun
                ,bofang
                ,jieshao
            from `7ph56346_gequxinxi`
            where(not exists (select
                id
                ,title
                ,picture
                ,zuozhe
                ,xqdz
                ,shoucang
                ,share
                ,pinglun
                ,bofang
                ,jieshao
            from `gequxinxi` where
                `gequxinxi`.id=`7ph56346_gequxinxi`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
