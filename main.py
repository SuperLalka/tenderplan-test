
from app.tasks import parse_page_task

example_urls = [
    "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1",
    "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2"
]


def run_parser():
    for url in example_urls:
        parse_page_task.delay(page_url=url)


if __name__ == "__main__":
    run_parser()
