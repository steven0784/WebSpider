from scrapy.spider import Spider
from scrapy.selector import Selector
from nytimes.items import MainItem
from scrapy.http import Request
import helper
import LinksAnalysis
import scrapymethods
class BasicSpider(Spider):
   name = 'basicspider'
   given_urls = ["http://www.cbc.ca","http://www.thestar.com/"]
   url_list = LinksAnalysis.find_category_links(given_urls)
   start_urls = url_list
   global keyword 
   keyword = 'sport'
   def parse(self, response):
      dict_list_items = []
      items = scrapymethods.start_scrapy(response, dict_list_items,keyword)
      return items
      #for index in range(len(items)):
      #   if items[index]["status"] == "link site":
      #      link = items[index]['url']
      #      request = Request(link, callback=self.parse_content)
      #      request.meta['list'] = items
      #      yield request
   
   def parse_content(self, response):
      items = response.meta['list']
      #item['body'] = response.url
      result_list = scrapymethods.start_scrapy(response, items, keyword)
      for index in range(len(result_list)):
         if result_list[index]["status"] == "link site":
            link = result_list[index]['url']
            request = Request(link, callback=self.parse_content)
            request.meta['list'] = result_list
      return result_list

