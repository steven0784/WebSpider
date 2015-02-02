# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field

from crawler.models import crawlData

class crawlDataItem(DjangoItem):
   # fields for this item are automatically created from the django model
   django_model = crawlData


class MybotItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass

class HolderItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	excerpts = scrapy.Field()
	links = scrapy.Field()

class MainItem(scrapy.Item):
	name = Field()
	url = Field()
	body = Field()
	status = Field()
	source = Field()