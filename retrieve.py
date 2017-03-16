import requests, json
from bs4 import BeautifulSoup

#TODO: This could totally be a generator
class HNParser(object):

	def __init__(self):
		self.base_link = 'https://news.ycombinator.com/news?p='
		self.page_limit = 2;
		self.text = ''

	def get_page(self, n):
		link = self.base_link + str(n)
		#TODO: Check status code
		r = requests.get(link)
		self.text = r.text

	def content_arr(self):
		soup = BeautifulSoup(self.text, 'lxml')
		page_rows = soup.find_all('tr', 'athing')
		content = []
		for page_row in page_rows:
			row_story = page_row.find('a', 'storylink')
			link = row_story.attrs['href']
			title = row_story.get_text()
			content.append({'link': link, 'title': title})
		return content 

class REDParser(object):

	def __init__(self):
		self.base_link = 'https://www.reddit.com/r/programming.json?count='
		self.page_limit = 2
		self.page_size = 25
		self.text = ''

	def get_page(self):
		link = self.base_link + str(self.page_limit * self.page_size)
		#TODO: Check status code
		r = requests.get(link)
		self.text = r.text

	def content_arr(self):
		page_content = json.loads(self.text)['data']['children']
		build_list = lambda acc, item: acc + [{'link': item['data']['url'], 'title': item['data']['title']}]
		content = reduce(build_list, page_content, []) 
		return content
		
		
# Quick Test
# hn = HNParser()
# hn.get_page(1)
# print hn.content_arr()
# hn.get_page(2)
# print hn.content_arr()
rd = REDParser()
rd.get_page()
print rd.content_arr()
