import os
import re

from bs4 import BeautifulSoup

import text_extraction
from grab_links import grab_links_from_page_as_list, grab_links_from_page_extra_info
from main_functions import get_text_from_url, getInp


def generate_file_from_url(url: str):
    text = get_text_from_url(url)
    if len(text) < 200:
        return False
    opened_file = open(find_free_filename("./generated/"), "w", encoding="utf-8")
    opened_file.write(text)
    opened_file.close()
    return True


def find_free_filename(directory, iteration=0):
    desired_name = directory + "file_" + str(iteration) + ".txt"
    if os.path.isfile(desired_name):
        return find_free_filename(directory, iteration=iteration + 1)
    return desired_name


def get_apnotes_url(index: int):
    return "https://apnotes.net/notes-12e/ch%d-12e.html" % index


def generate_apnotes_files(count: int):
    for i in range(1, count + 1):
        url = get_apnotes_url(i)
        print(url)
        generate_file_from_url(url)


def generate_wiki_files(count: int):
    generated = 0
    while generated < count:
        if generate_file_from_url("https://en.wikipedia.org/wiki/Special:Random"):
            generated += 1


def generate_files_from_urls(urls):
    for url in urls:
        generate_file_from_url(url)


forbidden = {"", "Main page", "Read", "Article"}


def is_content_link(url, label):
    if label in forbidden or ("ikipedia" in label or "rticle" in label):
        return False
    if not url.startswith("/wiki/"):
        return False
    if ":" in url:
        if "/wiki/Category" in url:
            return True
        return False
    trimmed = url.strip("/wiki/")
    for c in trimmed:
        if not c.isalnum() and c != "_":
            return False
    return True


def generate_labeled_wiki_doc(url):
    raw_html = getInp(url)
    soup = BeautifulSoup(raw_html, "html.parser")
    useful_text = text_extraction.get_text(soup)
    urls = list(grab_links_from_page_extra_info(url, html=raw_html))
    urls = filter(lambda x: is_content_link(x[0], x[1]), urls)
    return urls


print("\n\n".join(str(x) for x in generate_labeled_wiki_doc("https://en.wikipedia.org/wiki/Special:Random")))
