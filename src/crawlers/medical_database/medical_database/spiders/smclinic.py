import scrapy
from scrapy.http.response import Response
from fake_headers import Headers
from scrapy_playwright.page import PageMethod


def abort_request(request):
    return request.resource_type == "image" or ".jpg" in request.url


class SmclinicSpider(scrapy.Spider):
    name = "smclinic"
    allowed_domains = ["smclinic.ru"]
    start_urls = ["https://www.smclinic.ru/diseases/"]

    headers = Headers(os="win", browser="chrome")

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "timeout": 40 * 1000
        },
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 12,
        "PLAYWRIGHT_ABORT_REQUEST": abort_request
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.smclinic.ru/diseases/",
            headers=self.headers.generate(),
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 12000)
                ]
            }
        )

    def parse(self, response: Response):
        hrefs = response.xpath('//div[@class="diseases-list__item"]/a/@href').getall()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(
                url=url,
                headers=self.headers.generate(),
                callback=self.parse_simptoms,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_timeout", 4800)
                    ]
                }
            )

