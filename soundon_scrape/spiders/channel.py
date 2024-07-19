import scrapy
from scrapy_playwright.page import PageMethod
from playwright.sync_api import sync_playwright
from scrapy_playwright.page import PageMethod

class ChannelSpider(scrapy.Spider):
    name = "channel_spider"
    start_urls = ['https://player.soundon.fm/p/511455c6-f5ee-4e8f-aac3-912b277c0efe']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                    playwright_page_methods = [
                        PageMethod('wait_for_load_state', 'networkidle'),
                        PageMethod('evaluate', 'window.__requests = []; window.XMLHttpRequest.prototype.open = function() { window.__requests.push(arguments); };'),
                        PageMethod('wait_for_timeout', 4000)
                    ],
                    errback=self.errback,
                )
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        requests = await page.evaluate("window.__requests")
        for req in requests:
            self.logger.info(f"Captured XHR request: {req}")
        await page.close()  

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

