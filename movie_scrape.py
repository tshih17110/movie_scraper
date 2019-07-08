from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import time
import logging
from threading import Thread
import sys

def linkScrape(q):
	"""Scrapes Metacritic for movie list urls depending on category given, and places into queue"""
	base = 'https://www.metacritic.com'
	req = Request('https://www.metacritic.com/browse/movies/score/metascore/90day/filtered?sort=desc', 
	headers={'User-Agent': 'Mozilla/5.0'})
	# req = Request(.category, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	parse = SoupStrainer(class_=['title'])
	profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)
	for url in profile.find_all('a', class_='title')[:25]:
		q.put(urllib.parse.urljoin(base, url.get('href')))
		# print(*links, sep = "\n")
	return q

def thread_scrape(url_queue):
	"""Queue to scrape each link in list of movie urls"""
	while True:
		url = url_queue.get()
		if url is None:
			break
		profile_scrape(url)
		url_queue.task_done()

def scraper_worker(q):
	while not q.empty():
		url = q.get()
		profile_scrape(url)
		q.task_done()

def profile_scrape(url):
	"""
	Scrapes the title, metascore, and user score from one movie
	Currently returns: title, metascore, user score, runtime, metacritic awards
	"""
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	parse = SoupStrainer(class_=['product_page_title oswald', 'score fl', 'runtime', 'ranking_title'])
	profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)

	title_info = profile.find('div', class_='product_page_title oswald').h1.text
	runtime = profile.find('div', class_='runtime').text.split(":")[1].strip()
	scores = profile.find_all('div', class_='score fl')
	metascore = scores[0].div.text
	try:
		userscore = scores[1].div.text
	except:
		userscore = "tbd"

	# awards = profile.find_all('div', class_='ranking_title')

	movie_dict = {"title": title_info, "metascore": metascore, "userscore": userscore, 
	"runtime": runtime}

	for x in movie_dict:
		if movie_dict[x] is None or movie_dict[x] == "tbd":
			movie_dict[x] = "N/A"

	# print(movie_dict["title"] + " || " + movie_dict["metascore"]
	# 	+ " || " + movie_dict["userscore"] + " || " + movie_dict["runtime"])
	print(movie_dict["title"] + "\n" +  "Metascore: " + movie_dict["metascore"]
		+ "\n" + "Userscore: " + movie_dict["userscore"] + "\n" + "Runtime: " + movie_dict["runtime"] + "\n" + "_________________")
	# return movie_dict["title"] + " || " + "Metascore: " + movie_dict["metascore"] + " || " + "USER SCORE: " + movie_dict["userscore"]
	sys.stdout.flush()

def profile_scrapeV2(url):
	"""
	Scrapes the title, metascore, and user score from one movie
	Currently returns: title, metascore, user score, runtime, metacritic awards
	"""
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	parse = SoupStrainer(class_=['product_page_title oswald', 'metascore_w larger movie positive', 'metascore_w user larger movie positive', 
		'runtime', 'ranking_title'])
	profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)

	title_info = profile.find('div', class_='product_page_title oswald').h1
	metascore_info = profile.find('div', class_='metascore_w larger movie positive')
	userscore_info = profile.find('div', class_='metascore_w user larger movie positive')
	runtime = profile.find('div', class_='runtime')
	# awards = profile.find_all('div', class_='ranking_title')

	movie_dict = {"title": title_info, "metascore": metascore_info, "userscore": userscore_info, "runtime": runtime}

	for x in movie_dict:
		if movie_dict[x] is None:
			movie_dict[x] = "N/A"
		elif x == 'runtime':
			movie_dict[x] = movie_dict[x].text.split(":")[1].strip()
		else:
			movie_dict[x] = movie_dict[x].text

	# return movie_dict["title"] + " || " + "Metascore: " + movie_dict["metascore"] + " || " + "USER SCORE: " + movie_dict["userscore"]
	print(movie_dict["title"] + " || " + movie_dict["metascore"])
	sys.stdout.flush()





start = time.time()
q = Queue()
movieUrls = linkScrape(q)

for i in range(10):
	worker = Thread(target=scraper_worker, args=(q,))
	# worker.daemon = True
	worker.start()
	time.sleep(.1)
q.join

end = time.time()
print('Time taken to scrape: {0:.2f} seconds'.format(end - start)) 