import re
from typing import Optional

import requests
from urllib.parse import urlparse
from xml.dom import minidom
from xml.dom.minidom import Element

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class BasePageParser(object):
    def __init__(self, page_url: str, page=None, *args, **kwargs):
        self.page_url = page_url
        self.page = page or self.get_soup_object()
        self.domain = urlparse(page_url).scheme + "://" + urlparse(page_url).netloc

        self.args = args
        self.kwargs = kwargs

    def get_soup_object(self) -> BeautifulSoup:
        rsp = requests.get(self.page_url).text
        soup = BeautifulSoup(rsp, features='html.parser')
        return soup

    def get_printed_docs_links(self) -> list:
        links = self.page.find_all('div', class_='registry-entry__header-mid__number')
        links = [self.domain + x.a.attrs['href'] for x in links]

        return [re.sub(
            r'notice/[\w\d]*/[\w\d]*/.*.html',
            'notice/printForm/viewXml.html',
            link
        ) for link in links]


class XMLParser(object):

    @staticmethod
    def get_headers() -> dict:
        ua = UserAgent()
        return {
            'accept': 'text/xml, */*',
            'user-Agent': ua.google,
        }

    def get_xml_object(self, doc_url) -> Element:
        rsp = requests.get(doc_url, headers=self.get_headers())
        assert rsp.status_code == 200, f'Unexpected response received from url: {doc_url}'
        return minidom.parseString(rsp.text)

    def get_publishDTInEIS(self, doc: Element) -> Optional[str]:
        return doc.getElementsByTagName('publishDTInEIS')[0].firstChild.nodeValue
