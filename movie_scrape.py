from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
from queue import Queue
import threading
import urllib.parse
import time
import sys
import profile_scrape

# defaultpage = 'https://www.metacritic.com/browse/movies/score/metascore/90day/filtered?sort=desc'
class MovieScraper():

	def __init__(self, threads):
		self.page = 'https://www.metacritic.com/browse/movies/score/metascore/90day/filtered?sort=desc'
		self.threads = threads

	def link_scrape(self, q):
		"""Scrapes Metacritic for movie list urls depending on category given, and places into queue"""
		base = 'https://www.metacritic.com'
		req = Request(self.page, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		parse = SoupStrainer(class_=['title'])
		profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)
		#Edit next line for amount of movies scraped
		for x in profile.find_all('a', class_='title')[:10]: 
			q.put(urllib.parse.urljoin(base, x.get('href')))
		return q

	def scraper_worker(self, q):
		while not q.empty():
			url = q.get()
			# self.profile_scrape(url)
			profile_scrape.movie_info(url)
			q.task_done()

	def multithread_scrape(self):
		q = Queue()
		movie_urls = self.link_scrape(q)
		for i in range(self.threads):
			worker = threading.Thread(target=self.scraper_worker, args=(movie_urls,))
			worker.start()
			time.sleep(.1)
		q.join

