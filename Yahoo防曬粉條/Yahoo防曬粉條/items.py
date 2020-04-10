import scrapy


class YahooItem(scrapy.Item):
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_category = scrapy.Field()
    product_source = scrapy.Field()
    product_images = scrapy.Field()
