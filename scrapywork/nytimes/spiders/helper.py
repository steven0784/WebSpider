from urlparse import urlparse

def check_url_duplicate(items, url):
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
          if items[listindex]['url'].strip():
              if items[listindex]['url'][-1] == '/':
                 cmp1 = items[listindex]['url'][:-1]
              else:
                 cmp1 = items[listindex]['url']
              if cmp1 == cmp2:
                 return listindex
      return -1
  else:
      return -1

def convert_to_list_of_str(item_list):
    newlist = []
    for item in item_list:
        newlist

def find_domain_url (url):
    '''(str) -> str
        return the domain url of given url
        >>>find_domain_url ('http://www.nytimes.com/sport')
        >>>http://www.nytimes.com
    '''
    output_url = urlparse(url)
    return output_url.scheme + "://" + output_url.hostname

def attach_url_with_name(url, domain_url):
    '''(obj, str, str) -> str
        check if given url is not a complete url,
        if not, return a combined with domain url
        else, return it
    '''
    #check url
    if url.startswith('http://'):
        return url
    else:
        if url.startswith('/'):
            return domain_url + url
        else:
            return domain_url + '/' + url

def check_url_exist(url):
    import urllib2
    try:
        urllib2.urlopen(url)
        return True
    except urllib2.HTTPError, e:
        return False

