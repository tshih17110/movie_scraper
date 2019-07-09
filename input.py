import sys
import time
from movie_scrape import MovieScraper

def main():
	input_thread = int(sys.argv[1])
	start = time.time()
	movies = MovieScraper(input_thread).multithread_scrape()
	end = time.time()
	print('Time taken to scrape: {0:.2f} seconds'.format(end - start))

main()