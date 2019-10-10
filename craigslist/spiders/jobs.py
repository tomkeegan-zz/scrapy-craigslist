# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            location = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")
            url = job.xpath('a/@href').extract_first()
            time = job.xpath('time/@datetime').extract_first()
            yield Request(url, callback=self.parse_page, meta={'title':title,'location':location,'url':url,'time':time})
        next_relative_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        next_url = response.urljoin(next_relative_url)
        yield Request(next_url, callback=self.parse)

    def parse_page(self, response):
        title = response.meta.get('title')
        location = response.meta.get('location')
        time = response.meta.get('time')

        description = "".join(line for line in response.xpath('//section[@id="postingbody"]/text()').extract())
        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()

        yield {
            'title': title,
            'location': location,
            'time': time,
            'description': description,
            'compensation': compensation,
            'employment_type': employment_type
        }
            
