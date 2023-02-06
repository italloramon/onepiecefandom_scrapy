import scrapy

class CharacterItem(scrapy.Item):
    name = scrapy.Field()
    chapter = scrapy.Field()
    episode = scrapy.Field()
    year = scrapy.Field()
    note = scrapy.Field()