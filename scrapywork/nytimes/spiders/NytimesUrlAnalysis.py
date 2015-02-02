import requests

class DataAnalysis(object):
    
    def __init__(self, urls, query, date_range='30daysago', page=1):
        self.urls = urls
        self.query = query
        self.date_range = date_range
        self.page = page
        self.searchlinks = []
        
    def _checkurls(self):
        for url in self.urls:
            if 'nytimes' in url:
                self.searchlinks += (self._NYtimesAnalyse(url))
            else:
                self.searchlinks += url
    
    def get_start_links(self):
        self._checkurls()
        return self.searchlinks
    
    def _NYtimesAnalyse(self, url):
        '''(str) -> list
        return search urls by given url
        '''
        #if the given url is http://www.nytimes.com
        if (url[-4:] == ".com" or url[-5:] == ".com/") and len(url) <= 23:
            return (self._NYtimesSearchSite(self.query, self.date_range, self.page))
        else:
            return [url]
        
    def _NYtimesSearchSite(self, query, date_range, page):
            search_url = 'http://query.nytimes.com/svc/cse/v2pp/sitesearch.json'
            params = {
                'query': "%s" % (query),
                'date_range_lower': '%s' % (date_range),
                'pt': 'article',
                'page' : '%s' % (page)
            }
            response = requests.get(search_url, params=params)
            data = response.json()
            result_list = []
            for result in data['results']['results']:
                result_list.append(result.get('og:url').encode('utf-8'))
            return result_list
