from celery import shared_task
from celery import task
import sys
import subprocess
sys.path.append('../mybot')
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from mybot.spiders.sitemapSpider import SiteMapSpider
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from .models import Session, resultLogData, crawlData
import os
os.environ['SCRAPY_SETTINGS_MODULE'] = 'mybot.settings'
from warc_option import *

def stop_reactor():
    reactor.stop()

class ReactorControl:

    def __init__(self):
        self.crawlers_running = 0

    def add_crawler(self):
        self.crawlers_running += 1

    def remove_crawler(self):
        self.crawlers_running -= 1
        if self.crawlers_running == 0 :
            reactor.stop()

def setup_domain(domain, keyword_list, source_list, reactor_control, sessionID, result_count):
    spider = SiteMapSpider(domain, keyword_list, source_list, sessionID, result_count)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor_control.remove_crawler, signal=signals.spider_closed)
    reactor_control.add_crawler()
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


@shared_task()
def crawl_domain(sessionID):
    session = Session.objects.get(id=sessionID)
    session.result_count+=1
    session.save()
    #p = subprocess.Popen(['scrapy', 'crawl','sitemapspider', '-a', monitor.url], cwd='../mybot')
    #p.wait()
    r = 0
    #dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    sources = session.sources.all()
    source_keywords = []
    source_urls = []
    set_keywords = set()
    for source in sources:
        for word in str(source.keywords).strip().split(','):
            set_keywords.add(word)
        source_keywords.append(source.name)
        source_urls.append(source.url)
    source_keywords = list(set_keywords)

    monitors = session.monitors.all()
    reactor_control = ReactorControl()
    for monitor in monitors:
        setup_domain(monitor.url,source_keywords, source_urls, reactor_control, sessionID, session.result_count)
    #crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    log.start(loglevel=log.DEBUG)
    log.msg("------------>Running reactor")
    result = reactor.run()
    print result
    log.msg("------------>Running stopped")
    allLog = resultLogData.objects.all()
    for x in allLog:
        if int(x.sessionID) == sessionID:
            r = 1;
    if r == 0:
        session = resultLogData(sessionID=sessionID)
        session.save()
    
    #want list of urls
    # all = crawlData.objects.all()
    # for cd in all:
    #     #Generates the WARC files in the WARC directory
    #     title = cd.article_title.encode('ascii', 'ignore').decode('ascii')
    #     warc_download(title, cd.article_url, sessionID, "Hits ")
    #from crawl import run_spider
    #return run_spider()
