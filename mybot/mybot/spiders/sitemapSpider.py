import scrapy
import urlparse
from mybot.items import MainItem, HolderItem, crawlDataItem
from scrapy.selector import Selector, XmlXPathSelector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from urlparse import urlparse as up2

class SiteMapSpider(scrapy.Spider):
	name = 'sitemapspider'
	# keyword = 'snow'
	# url_match = 'twitter.com'

	SITEMAP_XPATH = '//a[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "site map")]'
	NEWS_CATEGORY_XPATH = '//li[a[contains(., "World")]]/parent::ul/li/a'

	def parse_article(self, response):
		items = []
		#item = MainItem()
		item = crawlDataItem()
		sel = Selector(response)
		sites = sel.xpath('//a')
		paragraphlist = sel.xpath('//p/text()').extract()
		for site in sites:
			addrnamelist = site.xpath('./text()').extract()
			addrlinklist = site.xpath('./@href').extract()
			if addrnamelist != []:
				for name in addrnamelist:
					str_name = name.encode('utf-8').strip()
					if addrlinklist != []:
						str_url = addrlinklist[0].encode('utf-8').strip()
					else:
						str_url = ''
					if self.keyword.lower() in str_name.lower():
						item['title'] = str_name
						item['link'] = str_url
						item['origin'] = self.find_domain_url(response.url)
						items.append(item.copy())
		if paragraphlist != []:
			for text in paragraphlist:
				if self.keyword.lower() in text.encode('utf-8').lower():
					indicater = self.check_url_duplicate(items, response.url)
					if indicater == -1:
						item['link'] = response.url
						item['body'] = text.encode('utf-8').strip()
						items.append(item.copy())
					else:
						items[indicater]['body'] = text.encode('utf-8').strip()
		return items
	
	def check_url_duplicate(self, items, url):
		'''(obj, list of dict, str) -> int
		-1 means False
		other int means True
		'''
		if url.strip():
			if url[-1] == '/':
			  	cmp2 = url[:-1]
			else:
			      cmp2 = url
			for listindex in range(len(items)):
				if items[listindex]['link'].strip():
					if items[listindex]['link'][-1] == '/':
						cmp1 = items[listindex]['link'][:-1]
					else:
						cmp1 = items[listindex]['link']
					if cmp1 == cmp2:
						return listindex
			return -1
		else:
			return -1

	def find_domain_url (self, url):
		'''(str) -> str
		return the domain url of given url
		>>>find_domain_url ('http://www.nytimes.com/sport')
		>>>http://www.nytimes.com
		'''
		output_url = up2(url)
		return output_url.scheme + "://" + output_url.hostname

	
	def parse_newspage(self, response):
		#self.log('We are parsing news page: %s' % response.url)
		
		#self.log(str(xpathlist))
		linkextractor = LinkExtractor(allow_domains=self.allowed_domains, restrict_xpaths = self.LINK_XPATHLIST)
		for link in linkextractor.extract_links(response):
			yield scrapy.Request(link.url, callback=self.parse_myarticle)

	def parse_myarticle(self, response):
		#self.log('We are parsing article: %s' % response.url)

		title = response.xpath('//title/text()').extract()[0]
		url = response.url

		# Parse <p> and <a> text for keyword
		for keyword in self.keywords:
			for paragraph in response.xpath('(//p | //a)/text()[contains(., "' + keyword + '")]').extract():
				crawldata = crawlDataItem()
				crawldata['article_title'] = title
				crawldata['article_url'] = url
				crawldata['ref_keyword'] = keyword
				crawldata['excerpts'] = paragraph
				crawldata['ref_link'] = None
				crawldata['in_sessionID'] = self.sessionID
				crawldata['in_resultID'] = self.resultID
				yield crawldata
		#if excerpts:
		#	self.log('Contents of keyword matches include: %s' % str(excerpts))

		# Parse <a> @href for link match
		for ref_link in self.ref_links:
			#linkextractor = LinkExtractor(allow=(ref_link), allow_domains=self.allowed_domains)
			for link in response.xpath('//p/a/@href[contains(., "'+ref_link+'")]').extract():
			#for link in linkextractor.extract_links(response):
				#self.log('Found a link at %s' % link.url)
				crawldata = crawlDataItem()
				crawldata['article_title'] = title
				crawldata['article_url'] = url
				crawldata['ref_link'] = link
				crawldata['excerpts'] = None
				crawldata['in_sessionID'] = self.sessionID
				crawldata['in_resultID'] = self.resultID
				yield crawldata

	def parse_sitemap(self, response):
		#self.log('We are parsing site map: %s' % response.url)
		linkextractor = LinkExtractor(allow_domains=self.allowed_domains, restrict_xpaths=self.NEWS_CATEGORY_XPATH)
		for link in linkextractor.extract_links(response):
			yield scrapy.Request(link.url, callback=self.parse_newspage)

		# news_sel = response.xpath('//li[a[contains(., "World")]]/parent::ul/li')
		# for url in news_sel.xpath('.//a/@href').extract():
		# 	url = urlparse.urljoin(response.url, url)
		# 	yield scrapy.Request(url, callback=self.parse_newspage)

	def __init__(self, starting_url=None, keywords=None, urls=None, sessionID=0, resultID=1, *args, **kwargs):
		super(SiteMapSpider, self).__init__(*args, **kwargs)
		if not (starting_url or keywords or urls):
			starting_url = 'http://www.nytimes.com'
			self.allowed_domains = [self.find_allowed_domain(starting_url)]
			self.start_urls = [starting_url]
		else:
			url = self.url_validate(starting_url)
			self.allowed_domains = [self.find_allowed_domain(url)]
			ref_links = []
			for each_url in urls:
				ref_links.append(self.find_allowed_domain(each_url))
			if url != 'invalid':
				self.start_urls = [url]
				self.ref_links = ref_links
				self.keywords = keywords
		self.sessionID = sessionID
		self.resultID = resultID
		self.LINK_XPATHLIST =['//p/a']
		for header_index in range(1, 7):
			self.LINK_XPATHLIST.append('//h'+str(header_index)+'/a')
			#remeber to check 404 in response
			#if response.status != 404 ,then ..
			
	def url_validate(self, url):
		result = ''
		output_url = up2(url.strip())
		if output_url.scheme != '':
			if output_url.hostname:
				if output_url.hostname.startswith('www.'):
					return url
				else:
					fix_url = 'http://www.' + url[6:]
					return self.url_validate(fix_url)
		else:
			fix_url = 'http://' + url
			return self.url_validate(fix_url)
		return 'invalid'

	def find_allowed_domain(self, url):
		result = ''
		output_url = urlparse.urlparse(url.strip())
		hostname = output_url.hostname
		if hostname:
			if hostname.startswith('www.'):
				result = hostname[4:]
			else:
				result = hostname
		return result
	
	def parse_xml(self, response):
		for link in response.selector.re(r'<loc>(.*)'):
			index = link.find(".xml")
			if index > 0:
				#self.log('xml is %s ' % (link[:index]+'.xml'))
			 	#yield scrapy.Request(link[:index]+'.xml', callback=self.parse_xml)
			 	pass
			else:
				index = link.find("</loc>")
				if index > 0: 
					self.log('chopped link is %s ' % link[:index])
					yield scrapy.Request(link[:index], callback=self.parse_myarticle)
				else:
					self.log('regular link is %s ' % link)
				 	yield scrapy.Request(link, callback=self.parse_myarticle)


	def parse_robot(self, response):
		#Sitemap: http://www.cp24.com/sitemap_news.xml
		for sitemap in response.selector.re(r'Sitemap: (.*)'):
			self.log("Site map is %s" % sitemap)			
			yield scrapy.Request(sitemap.strip(), callback=self.parse_xml)

	def parse(self, response):
		#self.log('We are at URL: %s' % response.url)
		yield scrapy.Request(response.url+'robots.txt', callback=self.parse_robot)
		linkextractor = LinkExtractor(allow_domains=self.allowed_domains, restrict_xpaths=self.SITEMAP_XPATH)
		for link in linkextractor.extract_links(response):
			yield scrapy.Request(link.url, callback=self.parse_sitemap)
