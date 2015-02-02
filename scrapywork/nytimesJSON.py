import requests

url = 'http://query.nytimes.com/svc/cse/v2pp/sitesearch.json'
params = {
    'query': "israel",
    'date_range_lower': '30daysago',
    'pt': 'article',
    'page' : '2'
}

response = requests.get(url, params=params)
data = response.json()
for result in data['results']['results']:
    print result.get('og:url')
