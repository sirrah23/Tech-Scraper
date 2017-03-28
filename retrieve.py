import requests, json
from bs4 import BeautifulSoup
from custom_exception import RequestException

class HNParser(object):

	def __init__(self):
		self.base_link = 'https://news.ycombinator.com'
		self.base_link_rq = 'https://news.ycombinator.com/news?p='
		self.page_limit = 2;

	def get_page(self, n):
		link = self.base_link_rq + str(n)
		r = requests.get(link)
		if r.status_code != requests.codes.ok:
			raise RequestException("A bad status code of " + str(r.status_code) + " was returned")
		return r.text

	def content_arr(self):
		for i in xrange(1, self.page_limit+1):
			page_content = self.get_page(i)
			soup = BeautifulSoup(page_content, "html.parser")
			items = soup.find_all('tr', 'athing')
			content = []
			for item in items:
				item_id = item.attrs['id']
				story = item.find('a', 'storylink')
				link = story.attrs['href']
				title = story.get_text()
				comment_link = self.base_link + '/item?id=' + item_id
				content.append({'link': link, 'title': title, 'source':'hn', 'comment_link': comment_link})
		return content 

class REDParser(object):

	def __init__(self):
		self.base_link = 'https://www.reddit.com'
		self.base_link_rq = 'https://www.reddit.com/r/programming.json?limit='
		self.page_limit = 2
		self.page_size = 25

	def get_content(self):
		link = self.base_link_rq + str(self.page_limit * self.page_size)
		r = requests.get(link)
		if r.status_code != requests.codes.ok:
			raise RequestException("A bad status code of " + str(r.status_code) + " was returned")
		return r.text

	def content_arr(self):
		content_text = self.get_content()
		page_content = json.loads(content_text)['data']['children']
		build_list = (
			lambda acc, item: 
			acc + [{'link': item['data']['url'],
			 		'title': item['data']['title'],
			 		'source': 'reddit',
			 		'comment_link': self.base_link + item['data']['permalink']
			 		}]
		)
		content = reduce(build_list, page_content, []) 
		return content
		
		
# Quick Test
# hn = HNParser()
# hn.get_page(1)
# print len(hn.content_arr())
# hn.get_page(2)
# print hn.content_arr()
# rd = REDParser()
# print rd.content_arr()