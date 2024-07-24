from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from soundon_scrape.spiders.soundon import MainPageSpider
from scrapy.utils.project import get_project_settings

def run_spider(spider_name, output_file):
    cmdline.execute(f"scrapy crawl {spider_name} -o {output_file}".split())


if __name__ == '__main__':
    settings = get_project_settings()
    print(settings.copy_to_dict())
    # run_spider("main_page_spider", "output.json")
    # process = CrawlerProcess()
    # process.crawl(MainPageSpider)
    # process.start()
