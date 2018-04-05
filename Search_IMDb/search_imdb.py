import sys
import requests
from bs4 import BeautifulSoup
from functools import reduce


URL = 'http://www.imdb.com/search/title?groups=top_1000'

# Clear out names
def names(string):
    names = [s for s in string.split(',') if len(s) > 1]
    for i in range(len(names)):
        if not names[i][0].isalpha():
            names[i] = names[i][1:]
    return names

# Extract title, directors and actors from a movie
def parse_movie(m):
    title = m.a.text
    t = m.text.replace('\n', '')
    d = t[t.find('Directo')+9:]
    directors = names(d[:d.find('|')]) 
    b = t.find('Stars')
    e = t.find('Votes')
    actors = names(t[b+6:e])
    return title, directors, actors

# Crawl the IMDb list of top 1000 movies
def load_movies():
	movies = []
	for i in range(1, 21):
		url = URL + '&page=' + str(i)
		response = requests.get(url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			for m in soup.find_all("div", {"class": "lister-item-content"}):
				t, d, a = parse_movie(m)
				m = {'title': t,
                 	'director': d,
                 	'actors': a}
				movies.append(m)
	return movies

# From a given movie extract all key words
def get_key_words(m):
    keys = m["title"].split(' ')
    keys += [x for d in m["director"] for x in d.split(' ')] 
    keys += [x for a in m["actors"] for x in a.split(' ')]
    keys = [k.lower() for k in keys]
    return keys


def build_index(movies):
    search_index = {}
    for m in movies:
        for key in get_key_words(m):
            if key in search_index:
                search_index[key].append(m)
            else:
                search_index[key] = [m]
    return search_index

# find all movies in the index
def find(keys, index):
    search_keys = keys.split(' ')
    results = []
    for key in search_keys:
    	movies = index.get(key.lower())
    	if movies:
        	results.append(set([m['title'] for m in movies]))
    if not results:
    	return []
    return reduce((lambda x, y: x & y), results)

def main():
	print('Loading Movies')
	movies = load_movies()
	if not movies:
		print("Couldn't load the movies")
		return
	print('Movies successfully loaded')

	search_index = build_index(movies)

	while True:
		inp = input("  Please enter a keyword to search: ")
		for m in find(inp, search_index):
			print('  -- ' + m)
	return

# Run	
main()