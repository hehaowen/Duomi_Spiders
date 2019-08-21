# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from ..items import JobsItem


class DoumiSpider(scrapy.Spider):
    name = 'doumi'
    allowed_domains = ['www.doumi.com']
    start_urls = ['http://www.doumi.com/cityselect/']

    def parse(self, response):
        urlss = response.xpath('//div[@class="all-city"]/dl//dd/a/@href').extract()[0:-1]
        for url in  urlss:
            yield Request(url, callback=self.url_parse)

    def url_parse(self,response):
        urlss = response.xpath('//div[@class="inner-wrap"]/dl[1]/dd/ul/li/ul/li/a/@href').extract()
        area = response.xpath('//div[@class="crumbs w"]/a[2]/text()').extract()[0].replace('招聘网', '')
        urls = []
        for url in urlss:
            if url == '/xa/':
                continue
            else:
                urls.append(url)
        for i,url in  zip(range(10),urls):
            url = 'http://www.doumi.com' + url
            yield Request(url, meta={'area': area}, callback=self.jobs_parse)

    def jobs_parse(self, response):
        area = response.meta['area']
        urls = response.xpath('//div[@class="jzList-txt-t"]/h3/a/@href').extract()
        for url in urls:
            yield Request('http://www.doumi.com' + url, meta={'area': area}, callback=self.jobdetail_parse)

    def jobdetail_parse(self, response):
        area = response.meta['area']
        title = response.xpath('//div[@class="clearfix"]/h2/text()').extract()[0]
        wage = response.xpath('//div[@class="salary"]/span//text()').extract()
        details = response.xpath('//div[@class="jz-d-l-b"]').extract()
        settlement = response.xpath('//div[@class="salary-tips"]/span[1]/text()').extract()[0]
        sort = response.xpath('//div[@class="salary-tips"]/span[2]/text()').extract()[0]
        people = response.xpath('//div[@class="salary-tips"]/span[3]/text()').extract()[0]
        company = response.xpath('//div[@class="cpy-name"]/a/@href').extract()[0]
        title = title.replace(' ', '').replace('\n', '').replace('\t', '')
        wages = ''
        for i in wage:
            wages += i
        wage = wages.replace(' ', '').replace('\n', '')
        settlement = settlement.replace(' ', '').replace('\n', '')
        sort = sort.replace(' ', '').replace('\n', '')
        people = people.replace(' ', '').replace('\n', '')
        yield Request('http://www.doumi.com' + company, meta={
            'title': title,
            'area': area,
            'wage': wage,
            'details': details,
            'settlement': settlement,
            'sort': sort,
            'people': people
        }, callback=self.company_parse)

    def company_parse(self, response):
        area = response.meta['area']
        title = response.meta['title']
        wage = response.meta['wage']
        details = response.meta['details']
        settlement = response.meta['settlement']
        sort = response.meta['sort']
        people = response.meta['people']
        company = response.xpath('/html/body/div[3]/div[1]/div[2]/div/h2/text()').extract()
        introduction = response.xpath('/html/body/div[3]/div[3]/div[1]/div').extract()
        item = JobsItem()
        item['area'] = area
        item['title'] = title
        item['wage'] = wage
        item['details'] = details[0]
        item['settlement'] = settlement
        item['sort'] = sort
        item['people'] = people
        item['company'] = company[0]
        item['introduction'] = introduction[0]
        yield item
