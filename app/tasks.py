
import celery

from app.celery_app import app as clr_app
from app.handler import BasePageParser, XMLParser


class ParseTendersPageTask(celery.Task):
    name = 'parse_page_task'

    def run(self, page_url: str) -> None:
        parser = BasePageParser(page_url)

        docs_links = parser.get_printed_docs_links()

        for doc_link in docs_links:
            parse_xml_doc_task.delay(doc_link)


class ParseXMLTask(celery.Task):
    name = 'parse_xml_doc_task'
    max_retries = 5
    default_retry_delay = 5 * 60

    def run(self, doc_url: str) -> None:
        parser = XMLParser()

        try:
            xml = parser.get_xml_object(doc_url)
        except AssertionError as err:
            print(err)
            raise self.retry()

        publish_DTInEIS = parser.get_publishDTInEIS(xml)

        print(f"{doc_url} | {publish_DTInEIS}")


parse_page_task = clr_app.register_task(ParseTendersPageTask())
parse_xml_doc_task = clr_app.register_task(ParseXMLTask())
