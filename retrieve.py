import requests, json
from bs4 import BeautifulSoup
from custom_exception import RequestException

#TODO: This could totally be a generator
class HNParser(object):

	def __init__(self):
		self.base_link = 'https://news.ycombinator.com/news?p='
		self.page_limit = 2;

	def get_page(self, n):
		link = self.base_link + str(n)
		#TODO: Check status code
		r = requests.get(link)
		if r.status_code != requests.codes.ok:
			raise RequestException("A bad status code of " + str(r.status_code) + " was returned")
		return r.text

	def content_arr(self):
		for i in xrange(1, self.page_limit+1):
			page_content = self.get_page(i)
			soup = BeautifulSoup(page_content, "html.parser")
			page_rows = soup.find_all('tr', 'athing')
			content = []
			for page_row in page_rows:
				row_story = page_row.find('a', 'storylink')
				link = row_story.attrs['href']
				title = row_story.get_text()
				content.append({'link': link, 'title': title, 'source':'hn'})
		return content 

class REDParser(object):

	def __init__(self):
		self.base_link = 'https://www.reddit.com/r/programming.json?count='
		self.page_limit = 2
		self.page_size = 25

	def get_content(self):
		link = self.base_link + str(self.page_limit * self.page_size)
		print link
		#TODO: Check status code
		r = requests.get(link)
		if r.status_code != requests.codes.ok:
			raise RequestException("A bad status code of " + str(r.status_code) + " was returned")
		return r.text

	def content_arr(self):
		content_text = self.get_content()
		page_content = json.loads(content_text)['data']['children']
		build_list = (
			lambda acc, item: 
			acc + [{'link': item['data']['url'], 'title': item['data']['title'],'source': 'reddit'}]
		)
		content = reduce(build_list, page_content, []) 
		return content
		
		
# Quick Test
hn = HNParser()
hn.get_page(1)
print len(hn.content_arr())
hn.get_page(2)
print hn.content_arr()
rd = REDParser()
print len(rd.content_arr())