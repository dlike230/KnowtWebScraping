from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request
import text_extraction


def getInp(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    response = urllib.request.urlopen(req).read()
    html = response.decode('utf-8', errors='ignore').strip()
    html = html.replace("\\n", '\n').replace("\\'", "'").replace("\'", "'").replace("\\r", " ").replace("\\t", " ")
    return html


def get_text_from_url(url):
    htext = getInp(url)
    soup = BeautifulSoup(htext, "html.parser")
    return text_extraction.get_text(soup)
