# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field() #文章的标题
    create_date = scrapy.Field() #文章的时间
    url = scrapy.Field() #文章的链接
    url_object_id = scrapy.Field() #经MD5编码后的url
    front_image_url = scrapy.Field() #文章封面图片的链接
    front_image_path = scrapy.Field() #封面图的下载路径
    praise_nums = scrapy.Field() #文章的点赞数
    comment_nums = scrapy.Field() #文章的评论数
    fav_nums = scrapy.Field() #文章的收藏数
    tags = scrapy.Field() #文章的标签
    content = scrapy.Field() #文章的内容