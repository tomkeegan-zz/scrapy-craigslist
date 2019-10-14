from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from craigslist.spiders.jobs import JobsSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(JobsSpider)
process.start()