import time
from xml.dom import minidom

import pytest
import requests
import validators
from bs4 import BeautifulSoup

from app.handler import BasePageParser
from main import example_urls


class TestClass:
    main_pages_content = []
    main_pages_soup_objects = []
    xml_docs_links = []
    xml_docs_text = []
    xml_docs_objects = []

    @pytest.mark.dependency()
    def test_service_availability(self):
        for url in example_urls:
            attempts = 0
            while True:
                assert attempts < 10

                rsp = requests.get(url)
                if rsp.status_code == 200:
                    self.main_pages_content.append(rsp.text)
                    break

                time.sleep(1)
                attempts += 1

    @pytest.mark.dependency(depends=["TestClass::test_service_availability"])
    def test_get_soup_object(self):
        for page in self.main_pages_content:
            try:
                soup = BeautifulSoup(page, features='html.parser')
            except Exception:
                assert False
            else:
                self.main_pages_soup_objects.append(soup)

    @pytest.mark.dependency(depends=["TestClass::test_get_soup_object"])
    def test_get_printed_docs_links(self):
        for page_data in zip(example_urls, self.main_pages_soup_objects):
            parser = BasePageParser(page_url=page_data[0], page=page_data[1])
            links = parser.get_printed_docs_links()

            for link in links:
                assert lambda x: validators.url(link)
                self.xml_docs_links.append(link)

    @pytest.mark.dependency(depends=["TestClass::test_get_printed_docs_links"])
    def test_xml_objects_availability(self):
        for doc_link in self.xml_docs_links:
            attempts = 0
            while True:
                assert attempts < 10

                rsp = requests.get(doc_link)
                if rsp.status_code == 200:
                    self.xml_docs_text.append(rsp.text)
                    break

                time.sleep(1)
                attempts += 1

    @pytest.mark.dependency(depends=["TestClass::test_xml_objects_availability"])
    def test_xml_objects(self):
        for doc_text in self.xml_docs_text:
            try:
                doc = minidom.parseString(doc_text)
            except Exception:
                assert False
            else:
                self.xml_docs_objects.append(doc)

    @pytest.mark.dependency(depends=["TestClass::test_xml_objects"])
    def test_get_publish_DTInEIS_from_xml_objects(self):
        for doc_object in self.xml_docs_objects:
            publish_DTInEIS = doc_object.getElementsByTagName('publishDTInEIS')[0].firstChild.nodeValue
            assert publish_DTInEIS is not None
