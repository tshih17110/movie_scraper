from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
import urllib.parse
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

		movie_dict = {"title": title_info, "metascore": metascore, "userscore": userscore, 
		"runtime": runtime}
		for x in movie_dict:
			if movie_dict[x] is None or movie_dict[x] == "tbd":
				movie_dict[x] = "N/A"
		print(movie_dict["title"] + "\n" +  "Metascore: " + movie_dict["metascore"]
			+ "\n" + "Userscore: " + movie_dict["userscore"] + "\n" + "Runtime: " + movie_dict["runtime"] + "\n" + "_________________")
		sys.stdout.flush()