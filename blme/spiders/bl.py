import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from blme.items import Article


class BlSpider(scrapy.Spider):
    name = 'bl'
    start_urls = ['https://www.blme.com/about-us/blme-news/']

    def parse(self, response):
        articles = response.xpath('//li[@class="news-item"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            link = article.xpath('.//a[@class="news-item-header"]/@href').get()
            title = article.xpath('.//span/text()[2]').get()
            if title:
                title = title.strip()
            date = article.xpath('.//span/strong/text()').get()
            if date:
                date = datetime.strptime(date.strip(), '%d %B %Y')
                date = date.strftime('%Y/%m/%d')
            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', response.urljoin(link))

            yield item.load_item()
