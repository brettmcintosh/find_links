from sys import argv
import requests
import bs4

def get_html_string(url):
	# returns url's html as string
	data = requests.get(url)
	return data.text

def make_link_list(url):
	# extracts all links from html 
	html_string = get_html_string(url)
	soup = bs4.BeautifulSoup(html_string)
	link_list = soup.find_all('a')
	return link_list

def get_all_links(base_url):
	
	raw_base_links = make_link_list('base_url')
	base_links = extract_absolute_path(raw_base_links)
	master_url_set = set(base_links)
	visited_urls = []
	links_to_visit = []

	# search_new_page for base_url
	# grabs all links
	# extract and normalize
	# add links to links to visit if not in visited urls
	while len(links_to_visit) > 0:


def search_new_page(url):
	for url in base_links:
		if url not in visited_urls:
			visited_urls.append(url)
			new_page = get_html_string(url)
			new_page_links = make_link_list(new_page)
			cleaned_new_page_links = extract_absolute_path(new_page_links)
			


def extract_absolute_path(raw_base_links):
	# normalizes URLs and removes external links
	cleaned_links = [raw_base_links[i].get('href') for i in range(len(raw_base_links))]
	relevant_links = []
	for link in cleaned_links:
		if link and len(link) > 0:
			if link[0] == '/':
				link = 'http://www.myvr.com' + link
			if 'myvr.com' not in link:
				relevant_links.append(link)
		
	return relevant_links

if __name__ == '__main__':

	get_all_links(str(argv[1]))