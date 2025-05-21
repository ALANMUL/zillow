# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowScraperItem(scrapy.Item):
    zpid = scrapy.Field()
    streetAddress = scrapy.Field()
    zipcode = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    price = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()
    livingArea = scrapy.Field()
    homeType = scrapy.Field()
    homeStatus = scrapy.Field()
