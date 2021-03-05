import scrapy

from scrapy.loader import ItemLoader
from ..items import BsmsmItem
from itemloaders.processors import TakeFirst


class BsmsmSpider(scrapy.Spider):
	name = 'bsmsm'
	start_urls = ['https://www.bsm.sm/it/news-bsm.php']

	def parse(self, response):
		post_links = response.xpath('//div[@class="titolo-news bold"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1//text()').get()
		description = response.xpath('//span[@itemprop="description"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="bold"]/text()').get()

		item = ItemLoader(item=BsmsmItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
