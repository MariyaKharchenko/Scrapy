import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0"]

    def parse(self, response:HtmlResponse):
        print(response.status, response.url)
        links = response.xpath("//a[@class='product-card__name']/@href").getall()
        for link in links:
            next_page = response.xpath("//div[@class='pagination-next']/a/@href").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        #_id = response.xpath("//div[contains(@class, 'articul')]").get()
        price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        url = response.url

        yield BooksparserItem(name=name, price=price, url=url) #_id=_id
