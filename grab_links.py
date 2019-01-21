from bs4 import BeautifulSoup, SoupStrainer

from main_functions import getInp


def grab_links_from_page(url, html=None):
    if html is None:
        html = getInp(url)
    for link in BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            yield link['href']


def grab_links_from_page_extra_info(url, html=None):
    if html is None:
        html = getInp(url)
    for link in BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            yield (link['href'], ''.join(link.findAll(text=True)))


def grab_links_from_page_as_list(url, html=None):
    temp = grab_links_from_page(url, html)
    return list(temp)
