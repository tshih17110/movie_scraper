from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
# from queue import Queue
import urllib.parse
import time
import logging
# from threading import Thread
import sys


def movie_info(movie_url):
		"""
		Scrapes title, metascore, userscore, and runtime from the movie page
		"""
		req = Request(movie_url, headers={'User-Agent': 'Mozilla/5.0'})
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
		# print (movie_dict["title"] + "\n" + "_________________")
		sys.stdout.flush()



























# from requests import get
# from bs4 import BeautifulSoup, SoupStrainer
# from urllib.request import Request, urlopen
# import time
# import sys

# """
# Scrapes the title, metascore, and user score from one movie
# Currently returns: title, metascore, user score, runtime, metacritic awards
# """
# def profileScrape(url):
# 	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# 	webpage = urlopen(req).read()
# 	parse = SoupStrainer(class_=['product_page_title oswald', 'metascore_w larger movie positive', 'metascore_w user larger movie positive', 
# 		'runtime', 'ranking_title'])
# 	profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)

# 	title_info = profile.find('div', class_='product_page_title oswald').h1
# 	metascore_info = profile.find('div', class_='metascore_w larger movie positive')
# 	userscore_info = profile.find('div', class_='metascore_w user larger movie positive')
# 	runtime = profile.find('div', class_='runtime')
# 	# awards = profile.find_all('div', class_='ranking_title')

# 	movie_dict = {"title": title_info, "metascore": metascore_info, "userscore": userscore_info, "runtime": runtime}

# 	for x in movie_dict:
# 		if movie_dict[x] is None:
# 			movie_dict[x] = "N/A"
# 		elif x == 'runtime':
# 			movie_dict[x] = movie_dict[x].text.split(":")[1].strip()
# 		else:
# 			movie_dict[x] = movie_dict[x].text


# 	# for y in awards:
# 	# 	print(y.a.text)


# 	# time = runtime.text.split(":")[1].strip()
	
# 	# print(movie_dict["title"] + " || " + "Metascore: " + movie_dict["metascore"] 
# 	# 	+ " || " + "USER SCORE: " + movie_dict["userscore"] + " || " + "RUNTIME: " + movie_dict["runtime"])

# 	# return movie_dict["title"] + " || " + "Metascore: " + movie_dict["metascore"] + " || " + "USER SCORE: " + movie_dict["userscore"]
# 	sys.stdout.flush()

# 	# def multithread_scrape():
# 	# 	for x in range(.thread_number):
# 	# 		worker = threading.Thread(target=)

# 	# """Returns a list of movie links from Metacritic"""
# 	# def movieLinks():
# 	# 	base = 'https://www.metacritic.com'
# 	# 	req = Request('https://www.metacritic.com/browse/movies/score/metascore/90day/filtered?sort=desc', 
# 	# 		headers={'User-Agent': 'Mozilla/5.0'})

# 	# 	webpage = urlopen(req).read()
# 	# 	parse = SoupStrainer(class_=['title'])
# 	# 	profile = BeautifulSoup(webpage, 'lxml', parse_only=parse)
# 	# 	links = []
# 	# 	for urls in profile.find_all('a', class_='title'):
# 	# 		links.append(urllib.parse.urljoin(base, urls.get('href')))
# 	# 	# print(*links, sep = "\n")
# 	# 	return links

# 	# """Scrapes a list of movie urls w/o the use of multithreading"""
# 	# def listScrape():
# 	# 	for x in movieLinks()[:10]:
# 	# 		movie_info(x)

# 	# """Basic thread scrape, no order preservation"""
# 	# def threadScrape():
# 	# 	threadList = []
# 	# 	for index in movieLinks()[:10]:
# 	# 		x = threading.Thread(target=movie_info, args=(index,))
# 	# 		x.daemon = True
# 	# 		threadList.append(x)
# 	# 		x.start()

# 	# 		# x.join()
# 	# 		# time.sleep(.1)
# 	# 	for x in threadList:
# 	# 		x.join()

# 	# def twoThreadScrapeV2():
# 	# 	threadList = []
# 	# 	movieList = movieLinks()
# 	# 	for index in movieList[:10]:
# 	# 		x = threading.Thread(target=movie_info, args=(index,))
# 	# 		x.daemon = True
# 	# 		threadList.append(x)

# 	# 		x.start()

# 	# 		# x.join()
# 	# 		# time.sleep(.1)
# 	# 	for x in threadList:
# 	# 		x.join()

# 	# def queueUrl(, q):
# 	# 	while True:
# 	# 		current = q.get()
# 	# 		if current is None:
# 	# 			break
# 	# 		.movie_info()

# 	# # def queueThreadScrape():
# 	# # 	q = Queue()

# 	# # 	for i in movieLinks[:10]:
# 	# # 		q.put(i)

# 	# # 	while not q.empty():

# #TEST
# # profileScrape('https://www.metacritic.com/movie/portrait-of-a-lady-on-fire')
# profileScrape('https://www.metacritic.com/movie/avengers-endgame')