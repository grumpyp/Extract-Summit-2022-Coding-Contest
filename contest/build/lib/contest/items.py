# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ContestItem(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    image_id = scrapy.Field()
    rating = scrapy.Field()

