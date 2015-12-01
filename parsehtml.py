#!/usr/bin/python

from datetime import date
import os,pickle,requests
from lxml import html
from pprint import pprint
import re


directory = str(date.today())
if not os.path.exists(directory) or not os.path.exists(directory+ "/results.p"):
    from topstories import *


results = pickle.load(open(directory+"/results.p", "r"))

urls = []
for article in results:
    url = article["url"]
    urls.append(url)

def scrape(url):
    page = requests.get(url)
    #print page.text.encode('utf-8')
    tree = html.document_fromstring(page.content)

    TEXT = tree.xpath("//p[@class=\"story-body-text story-content\"]/text() | //p[@class=\"story-body-text story-content\"]/*/text()".encode('utf-8'))

    filename = url.split("/")[-1].split(".")[0] + ".txt"
    f = open(directory + "/" + filename, "w")

    PROCESSED_TEXT = []
    for text in TEXT:
        text += "\n"
        text = text.encode('ascii', 'ignore')

        if PROCESSED_TEXT and PROCESSED_TEXT[-1].strip()[-1] != ".":
            PROCESSED_TEXT[-1] = PROCESSED_TEXT[-1].strip() + " " + text
            PROCESSED_TEXT[-1].replace("  ", " ")
        else:
            PROCESSED_TEXT.append(text)
    TEXT = PROCESSED_TEXT

    for text in TEXT:
        f.write(text)
    f.close()

    """
    f = open(directory + "/" + filename + ".html", "w")
    f.write(page.text.encode('utf-8'))
    f.close()
    """
    print url

for url in urls:
    scrape(url)    
