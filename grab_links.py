from bs4 import BeautifulSoup, SoupStrainer

from main_functions import getInp


def grab_links_from_page(url):
    html = getInp(url)
    for link in BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            print(link['href'])