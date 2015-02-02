from scrapy.spider import Spider
from scrapy.selector import Selector
import scrapy
from nytimes.items import NytimesItem
from NytimesUrlAnalysis import DataAnalysis
import requests


class NytimesSpider(Spider):
    name = "nytimes"
    allowed_domains = ["http://www.nytimes.com/"]
    #DataAnalyse(urls, query, date_range='30daysago', page=1)
    make_urls = DataAnalysis(["http://www.nytimes.com/"], 'israel')
    
    start_urls = make_urls.get_start_links()


    #quary format http://query.nytimes.com/search/sitesearch/#/quary/
    def parse(self, response):
        items = []
        item = NytimesItem()
        sel = Selector(response)
        classcontents = sel.xpath('//div/@class').extract()
        classnamelist = []
        for content in classcontents:
            if 'story' in content.encode('utf-8'):
                classnamelist.append(content.encode('utf-8'))
        body_content = []
        for classname in classnamelist:
            if 'body' in classname or 'content' in classname:
                body_content.append(classname)
                
        for i in body_content:
            ubody = sel.xpath('//div[@class="%s"]' % (i)).extract()
            body = []
            for stuff in ubody:
                body.append(stuff.encode('utf-8'))
            item['body'] = body
            items.append(item.copy())
        return items
