# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem
import re
from ArticleSpider.util.common import get_md5
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/page/538/']#需要爬的所有url

    def parse(self, response):
        """
        1.获取文章列表中的文章url，并交给scrapy下载后解析
        2.获取下一页的url，下载后，交给本parse函数
        :param response: 
        :return: 
        """
        #获得列表页中所有的文章url
        post_nodes = response.xpath('//div[@id="archive"]/div/div/a')
        for post_node in post_nodes:
            #获取文章封面图的url
            image_url = parse.urljoin(response.url, post_node.xpath('img/@src').extract_first(""))
            #获取文章的urlrl
            post_url = post_node.xpath('@href').extract_first("")
            #使用parse的urljoin可以防止有些url是相对路径
            yield Request(url = parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_article)
            #提取下一页的url
            next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first("")
            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)




    def parse_article(self, response):
        article_item = JobboleArticleItem();
        front_image_url = response.meta.get("front_image_url", "")
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").replace("·", "").strip()
        praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first("")
        fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first("")
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else :
            fav_nums = 0
        comment_nums = response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract_first("")
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        else :
            comment_nums = 0
        content = response.xpath('//div[@class="entry"]').extract_first("")
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [item for item in tag_list if not item.strip().endswith("评论")]
        tags = ",".join(tag_list)
        article_item["title"] = title;
        article_item["create_date"] = create_date
        article_item["url"] = response.url  # 文章的链接
        article_item["url_object_id"] = get_md5(response.url)  # 经MD5编码后的url
        article_item["front_image_url"] = [front_image_url]  # 文章封面图片的链接
        article_item["praise_nums"] = praise_nums  # 文章的点赞数
        article_item["comment_nums"] = comment_nums  # 文章的评论数
        article_item["fav_nums"] = fav_nums  # 文章的收藏数
        article_item["tags"] = tags  # 文章的标签
        article_item["content"] = content  # 文章的内容

        #通过ItemLoader加载item
        item_loader = ItemLoader(item=article_item, response=response)
        item_loader.add_xpath("title", )
        item_loader.add_value("url", response.url)
        yield article_item




