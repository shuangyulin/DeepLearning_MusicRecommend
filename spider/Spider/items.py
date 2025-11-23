# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class GequxinxiItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 图片
    picture = scrapy.Field()
    # 作者
    zuozhe = scrapy.Field()
    # 详情地址
    xqdz = scrapy.Field()
    # 收藏
    shoucang = scrapy.Field()
    # 分享
    share = scrapy.Field()
    # 评论
    pinglun = scrapy.Field()
    # 播放
    bofang = scrapy.Field()
    # 介绍
    jieshao = scrapy.Field()

class FensixinxiItem(scrapy.Item):
    # 歌曲名称
    name = scrapy.Field()
    # 粉丝地址
    fsdz = scrapy.Field()
    # 粉丝名称
    fsmc = scrapy.Field()
    # 粉丝头像
    fstx = scrapy.Field()
    # 所在地区
    szdq = scrapy.Field()
    # 个人介绍
    grjs = scrapy.Field()

class GedaninfoItem(scrapy.Item):
    # 歌单名称
    gdname = scrapy.Field()
    # 图片
    imgurl = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 歌单ID
    gdid = scrapy.Field()
    # 播放量
    playcount = scrapy.Field()
    # 订阅量
    subscribedcount = scrapy.Field()
    # 创建时间
    cjtime = scrapy.Field()
    # 详情地址
    detailurl = scrapy.Field()

class SonginfoItem(scrapy.Item):
    # 歌曲标题
    songtitle = scrapy.Field()
    # 时长
    shichang = scrapy.Field()
    # 歌手
    singer = scrapy.Field()
    # 专辑
    zhuanji = scrapy.Field()
    # 歌单ID
    gdid = scrapy.Field()
    # 详情地址
    detailurl = scrapy.Field()

