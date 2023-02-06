import scrapy

from onepiecefandom_scrapy.items import CharacterItem

class OpSpider(scrapy.Spider):
    name = 'characters'
    start_urls = [
        'https://onepiece.fandom.com/wiki/List_of_Canon_Characters#M'
    ]

    def parse(self, response, **kwargs):
        table = response.xpath('//*[@class="wikitable sortable"]')

        rows = table.xpath('//tr')

        for row in rows:
            char_item = CharacterItem()
            try:
                ## If the note is not empty, then correct the note to a string
                if row.xpath('td[6]//text()').extract() != None:
                    note = self.correct_notes(row.xpath('td[6]//text()').extract())
            except:
                note = ""
            ## If the name is None, then skip this row
            if row.xpath('td[2]//text()').extract_first() != None:
                ## If the name is Acrobatic Fuwas, then stop, because this is a table that we not want
                if row.xpath('td[2]//text()').extract_first() == 'Acrobatic Fuwas':
                    break

                char_item['name'] = row.xpath('td[2]//text()').extract_first()
                char_item['chapter'] = row.xpath('td[3]//text()').extract_first()
                char_item['episode'] = row.xpath('td[4]//text()').extract_first()
                char_item['year'] = row.xpath('td[5]//text()').extract_first()
                char_item['note'] = note

                yield char_item
    
    def correct_notes(self, notes = ['\n']):
        notecorrect = ""
        if notes[0] == '\n':
            return notecorrect
        else:
            notecorrect = ""
            for s in notes:
                if s != '\n':
                    notecorrect += s
            return notecorrect