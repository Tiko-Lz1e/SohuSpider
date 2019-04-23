import scrapy
import json
import time

from SohuSpider import spiders
from SohuSpider.items import sohuItem
from SohuSpider.spiders.channel_get import channel_list
from SohuSpider.spiders.channel_get import channels
import pymongo


class SohuSpider(scrapy.Spider):
    name = "sohu"
    allowed_domains = ["m.sohu.com"]
    start_urls = channel_list

    def parse(self, response):
#        filename = response.url.split("/")[-1]
        sites = json.loads(response.body_as_unicode())
        item = sohuItem()
        for site in sites['data']:
            if 'title' in site:  # 通过广告没有title信息的特点进行广告过滤
                item['title'] = site['title']   # 文章标题
                item['url'] = 'http://www.sohu.com' + site['url']  # 获取完整url
                # 根据搜狐时间戳获取真正发布时间
                item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(site['publicTime']/1000))
                item['channel'] = channels[response.url]  # 进行频道url和名称配对
                item['author'] = site['authorName']     # 文章来源媒体
                item['personalPage'] = site['personalPage']  # 来源媒体个人页面
                yield item

#        with open(filename, 'wb') as f:
#            f.write(response.body)

