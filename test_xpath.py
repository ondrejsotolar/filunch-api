import json
import os
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
import openai
import requests
from lxml import html, etree
from lxml.cssselect import CSSSelector
from bs4 import BeautifulSoup
from xml.sax import saxutils
import re
import ast

drevak_xpath = '//*[@id="menu"]'
url = "https://udrevaka.cz/denni-menu/"
response = requests.get(url)
tree = html.fromstring(response.content)
content_elements = tree.xpath(drevak_xpath)
pr = "".join([re.sub(r'\s{2,}', ' ', ''
                     .join(element.xpath(".//text()")).strip())
              for element in content_elements])
print(pr)