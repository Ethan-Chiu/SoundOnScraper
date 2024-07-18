import scrapy
from scrapy_playwright.page import PageMethod
from playwright.sync_api import sync_playwright

class MainPageSpider(scrapy.Spider):
    name = "main_page_spider"
    """ allowed_domains = ["player.soundon.fm"] """
    """ start_urls = ['https://player.soundon.fm/']  """

    def start_requests(self):
        url = "https://player.soundon.fm/browse/"
        yield scrapy.Request(url, meta=dict(
			playwright = True,
			playwright_include_page = True, 
            playwright_page_methods = [PageMethod('wait_for_selector', 'a.so-browse-podcast')],
      		errback=self.errback,
		))

    async def scroll_to_bottom(self, page):
        previous_height = 0 
        current_height = 0
        while True:
            await page.evaluate(f'window.scrollTo(0, {current_height + 100})')
            await page.wait_for_timeout(2000)# Wait for content to load, adjust timeout as needed

            # Check the current scroll height
            current_height = await page.evaluate('window.scrollY')
            if current_height == previous_height:
                break
            previous_height = current_height

    async def scroll_horizontally_in_containers(self, page, container_selector):
        container_elements = await page.query_selector_all(container_selector)
        for container in container_elements:
            scroll_width = await page.evaluate('(container) => container.scrollWidth', container)
            current_width = 0
            while True:
                # Scroll right
                await page.evaluate('(container) => container.scrollBy({ left: 1000, behavior: "smooth" })', container)
                await page.wait_for_timeout(2000)# Wait for content to load, adjust timeout as needed
                """ await page.wait_for_load_state('load')  # Wait for content to load, adjust timeout as needed """
                current_width += 1000

                if current_width > scroll_width:
                    break

    async def scroll_to_element(self, page, element_selector):
        elements = await page.query_selector_all(element_selector)
        while len(elements) != 0:
            for element in elements:
                await page.evaluate('(element) => element.scrollIntoView()', element)
                await page.wait_for_timeout(200) 
            elements = await page.query_selector_all(element_selector)


    async def parse(self, response):
        page = response.meta["playwright_page"]

        """ await self.scroll_to_bottom(page) """

        """ await page.screenshot(path="screenshot.png") """

        """ await self.scroll_horizontally_in_containers(page, 'div.so-browse-channel > div:nth-child(4) > div:nth-child(1)') """

        await self.scroll_to_element(page, 'div.lazyload-placeholder')
         
        await self.scroll_to_element(page, 'span.react-loading-skeleton')

        # Extract channel URLs
        channel_elements = await page.query_selector_all('a.so-browse-podcast')  # Adjust the selector as needed
        channel_urls = [await element.get_attribute('href') for element in channel_elements]

        """ channel_urls = response.css('a::attr(href)').extract() """
        for url in channel_urls:
            yield {"channel_url": url} 

            """ yield response.follow(url, self.parse_channel) """

    """ def parse_channel(self, response): """
    """     # Extract episode URLs """
    """     episode_urls = response.css('a::attr(href)').re(r'/p/\d+/episodes/\d+') """
    """     for url in episode_urls: """
    """         yield {'episode_url': response.urljoin(url)}     """

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

