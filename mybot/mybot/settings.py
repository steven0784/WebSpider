# -*- coding: utf-8 -*-

# Scrapy settings for mybot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
sys.path.insert(0, '../WebSpider')
os.environ['DJANGO_SETTINGS_MODULE'] = 'WebSpider.settings'
BOT_NAME = 'mybot'
SPIDER_MODULES = ['mybot.spiders']
NEWSPIDER_MODULE = 'mybot.spiders'
ITEM_PIPELINES = {
    'mybot.pipelines.CleanSpace': 900,
    #'mybot.pipelines.DuplicatesPipeline': 500,
    'mybot.pipelines.MybotPipeline': 1000
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mybot (+http://www.yourdomain.com)'
