from sys import argv
import requests
import bs4
from urlparse import urlparse


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


def extract_domain(base_url):
    # extract the domain from the url
    parsed_url = urlparse(base_url)
    return parsed_url


def get_all_links(base_url):
    # find all links at base_url and and add them to the search queue
    links_to_visit = search_new_page(str(base_url))

    # keeps track of all urls that have been searched
    visited_urls = set()

    # search links recursively until all links have been searched
    while len(links_to_visit) > 0:
        current_page = links_to_visit.pop()
        urls = search_new_page(current_page)
        for url in urls:
            if url not in visited_urls:
                visited_urls.add(url)

    print '\n\nFound %d internal links at %s.' % (len(visited_urls), base_url)
    return visited_urls


def search_new_page(url):
    # get all links on page at url
    print 'Finding links at %s' % url
    new_page_links = make_link_list(url)
    # parse here
    parsed_url = extract_domain(url)
    cleaned_new_page_links = extract_absolute_path(new_page_links, parsed_url)
    links_on_page = set(cleaned_new_page_links)

    return links_on_page


def extract_absolute_path(raw_base_links, parsed_url):
    # normalizes URLs and removes external links
    cleaned_links = [raw_base_links[i].get('href') for i in range(len(raw_base_links))]
    relevant_links = []
    for link in cleaned_links:
        if link and len(link) > 0:
            # convert relative path to absolute
            if link[0] == '/':
                link = parsed_url.scheme + '://' + parsed_url.netloc + link
            # check if link is internal and not an id, data uri, etc.
            if '.'.join(parsed_url.netloc.split('.')[-2:]) in link and 'http' in link:
                relevant_links.append(link)

    return relevant_links


if __name__ == '__main__':
    if len(argv) <= 1:
        print 'Enter an absolute url after the command, e.g. python find_links.py http://www.google.com'

    else:
        for number, link in enumerate(get_all_links(str(argv[1]))):
            print number, link