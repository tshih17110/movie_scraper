from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
from queue import Queue
import threading
import urllib.parse
import profile_scrape
import time

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
		for x in profile.find_all('a', class_='title')[:30]: 
			q.put(urllib.parse.urljoin(base, x.get('href')))
		return q

	def scraper_worker(self, q):
		"""Queue for scraping"""
		while not q.empty():
			url = q.get()
			profile_scrape.movie_info(url)
			q.task_done()

	def multithread_scrape(self):
		"""Multithreaded scraper compiling previous functions"""
		q = Queue()
		movie_urls = self.link_scrape(q)
		for i in range(self.threads):
			worker = threading.Thread(target=self.scraper_worker, args=(movie_urls,))
			worker.daemon = True
			worker.start()
			time.sleep(.5)
		q.join()

