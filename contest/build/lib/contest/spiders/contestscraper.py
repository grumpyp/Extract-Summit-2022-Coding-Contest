import scrapy
from contest.items import ContestItem
import re


class ContestscraperSpider(scrapy.Spider):
    name = 'contestscraper'
    allowed_domains = ['web-5umjfyjn4a-ew.a.run.app/clickhere']
    start_urls = ['https://web-5umjfyjn4a-ew.a.run.app/clickhere']
    
    def __init__(self) -> None:
        super().__init__()
        # str UUID "938ca07a-066b-4eb1-b49e-c0d4124557ea"
        # item_id = 
        # str, no leading or trailing spaces, e.g. "Sunset Song"
        # name = 
        #  UUID (str) of the non-thumbnail main item image, e.g "e5f1afa0-d044-4889-bd67-3eb6db4f598c", or None if no image accociated with item
        # image_id = 
        # # str, no leading or trailing spaces, e.g. "Perennial"
        # rating = 
        self.base_url = 'https://web-5umjfyjn4a-ew.a.run.app' 
        self.item_ids = []
        self.names = []
        self.image_ids = []
        self.ratings = []
    
    def santize(self, to_santize):
            # print(to_santize)
            # sant tumb img
            if to_santize[:9] == "/gen/thum":
                id = re.match(r'^\/gen\/thumb_(.*)\..*$', to_santize)
            # sant main img
            else:
                id = re.match(r'^\/gen\/(.*)\..*$', to_santize)
            return id.group(1)

    def parse_followed(self, response, item):
        contestitem = item
        try:
            contestitem['img_id'] = self.santize(response.xpath('//div[@class="container"]//img//@src').get())
            # self.image_ids.append(img_id)
            contestitem['rating'] = response.xpath('//div[@class="container"]//p[contains(.,"Rating")]/span/text()').get()
            # self.ratings.append(rating)
        except Exception:
            pass
        
        yield contestitem

    def parse(self, response):
        contestitem = ContestItem()

        for item in response.xpath('//div[@class="row"][1]//div[@class="col-md-6"]//div[@class="gtco-icon"]'):
            try:
                contestitem['item_id'] = self.santize(item.xpath('.//img//@src').get())
                # self.item_ids.append(item_id)
            except Exception:
                pass
        

        for item in response.xpath('//div[@class="row"][1]//div[@class="col-md-6"]//div[@class="gtco-copy"]'):
            try:
                contestitem['name'] = item.xpath('.//h3').get()
                # self.names.append(name)
                link = self.base_url + str(item.xpath('.//a/@href').get())
                
                # crawl landing
                yield scrapy.Request(
                     url=link,
                     callback=self.parse_followed,
                     dont_filter=True,
                     cb_kwargs={'item': contestitem})

            except Exception:
                pass
        
        next_page = str(response.xpath('//div[@class="row"][2]//a[contains(.,"Next Page")]/@href').get())
        if next_page:
             yield scrapy.Request(
                      url=next_page,
                      callback=self.parse,
                      dont_filter=True)

        



