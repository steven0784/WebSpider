def _check_url_duplicate(items, url):
##    if url.strip():
##        if url[-1] == '/':
##            cmp2 = url[:-1]
##        elif "?" in url:
##            for i in range(len(url)):
##                if url[i] == "?":
##                    cmp2 = url[:i]
##        else:
##            cmp2 = url
##        for listindex in range(len(items)):
##            url_item = items[listindex]['url']
##            if url_item.strip():
##                if url_item[-1] == '/':
##                    cmp1 = url_item[:-1]
##                elif "?" in url_item:
##                    for i in range(len(url_item)):
##                        if url_item[i] == "?":
##                            cmp1 = url_item[:i]
##                else:
##                    cmp1 = url_item
##                    
##                if cmp1 == cmp2:
##                    return listindex
##            else:
##                return -1
##    else:
##        return -1

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

if __name__ == "__main__":
    items = [{"url":"http://www.yahoo.ca", "other":"sdescsdfc"},
             {"url":"http://www.nytimes.ca", "other":"sdescsdfc"},
             {"url":"http://www.nba.ca/", "other":"sdescsdfc"},
             {"url":"http://www.google.ca?q=23423", "other":"sdescsdfc"},
             {"url":"http://www.csien.com/", "other":"sdescsdfc"},
             {"url":"http://www.google.ca", "other":"sdescsdfc"},
             {"url":"http://www.cmnm.ca", "other":"sdescsdfc"},
             {"url":"http://www.gosd.ca", "other":"sdescsdfc"},
             {"url":"", "acs":"acs"}]
    x = _check_url_duplicate(items, 'http://www.news.com/')
    y = _check_url_duplicate(items, 'http://www.google.ca')
    p = _check_url_duplicate(items, 'http://www.google.ca/')
    z = _check_url_duplicate(items, '')
    m = _check_url_duplicate(items, 'http://www.google.ca?q=csdf')
    q = _check_url_duplicate(items, 'http://www.news.com#@$@#%@#/')
    print (x,y,p,z,m,q)
#
