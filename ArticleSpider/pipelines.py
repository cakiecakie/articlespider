# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):

        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("article.json", 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spder_closed(self, spider): #当爬虫结束时调用，关闭文件
        self.file.close()

class JsonExportPipeline(object):
    #调用scrapy自身的jsonexport 导出json文件
    def __init__(self):
        self.file = open('articleExport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spoder(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'miaobeichen1993', 'article', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO article_item(title, url, url_object_id, create_date, fav_nums)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]))
        self.conn.commit()

#目前仍有问题
class MysqlTwistedPipeline(object): #使用Twisted提供的异步操作来完成数据的写入
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings): #用来读取setting文件
        dbparms = dict(
        host = settings["MYSQL_HOST"],
        dbname = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_USER"],
        passwd = settings["MYSQL_PASSWD"],
        charset = "utf8",
        cursorclass=MySQLdb.cursors.DictCursor,
        use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error) #处理异常

    def handle_error(self, failure):
        #处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
        INSERT INTO article_item(title, url, create_date, fav_nums)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))






class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item  #要把处理过的item返回出去，以便其他的pipeline继续操作