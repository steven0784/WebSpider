For mainspider.py
To see the result 
----
run "scrapy crawl mainspider -o main.csv -t csv"
----

1. get start_urls and keyword
2. in parse function, call _start() to scrapy link that contains keyword, and then scrapy paragraph that contains keyword. list will return [] if no stuff contains keyword
3. Then _start() will return a list that contains dicts 
4. in parse() it will send all scraped urls to parse_content function for rescrapy.

===================================
For Nytimes part
---
"scrapy crawl  nytimes -o article.csv -t csv"
---

1.nytimes now scrapy all <div> tags that contains 'story' in its class attribute

2. The demon of JSON works on nytimes is in this directory called 
nytimesJSON.py
run it to see how it works


==================================
For google search engine
---
googleSearch.py will show how it works
However, it's not stable, it will return Null when u run multiple times
and even u get all urls, some are not what you want
===============
remark: see the way of grab info from JSON in google is different than Nytimes


===================================
For check_dupli.py
---------------
if u don't understand what does my _check_url_duplicate
do in MainSpider.py
Here is a test case


===================================
For selenium libary function
----
some one said it works for getting page source after excuted javascript
but it seems have import error that they shows in example

just use pip install selenium to install
tryfirefox.py will shows that


===================================
For googlebs4.py
---
The tutorial of search from google by beautifulsoup.
it seems work, but sometime it still get banned
it will recieve some QA82NCSDMF stuff as result sometimes

====================================
just ignore the search.py file















