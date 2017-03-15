import requests
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

# Quick Test
hn = HNParser()
hn.get_page(1)
print hn.content_arr()
hn.get_page(2)
print hn.content_arr()