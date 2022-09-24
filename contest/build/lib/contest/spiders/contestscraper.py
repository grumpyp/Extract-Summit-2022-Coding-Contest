import scrapy
from contest.items import ContestItem
import re
import requests


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
            if to_santize[:5] == "/gen/":
                id = re.match(r'^\/gen\/(.*)\..*$', to_santize)
            # sant main img
            # else:
            #     id = re.match(r'^\/gen\/(.*)\..*$', to_santize)
            # sant item
            else:
                id = re.match(r'^\/item\/(.*)', to_santize)
            return id.group(1)

    def parse_followed(self, response, contestitem):
        contestitem = contestitem
        item = ContestItem()
        try:
            contestitem['img_id'] = self.santize(response.xpath('//img//@src').get())
        except Exception:
            contestitem['img_id'] = None
        try:
            # self.image_ids.append(img_id)
            contestitem['rating'] = response.xpath('//div[@class="container"]//p[contains(.,"Rating")]/span/text()').get()
            if response.xpath('//span[@class="price"]'):
                # print("xxxxx"* 100)
                data = str(response.xpath('//span[@class="price"]//@data-price-url').get())
                # print(data)
                r = requests.get(self.base_url + data)
                # print("xxxxx"* 100)
                # print(r.json())
                # print("xxxxx"* 100)
                contestitem['rating'] = r.json()['value']
            # self.ratings.append(rating)
        except Exception:
            print("wu")

        if contestitem.get('img_id'):
            item['image_id'] = contestitem['img_id']
        else:
            item['image_id'] = None
        if contestitem.get('rating'):
            item['rating'] = contestitem['rating']
        if contestitem.get('name'):
            item['name'] = contestitem['name']
        if contestitem.get('item_id'):
            item['item_id'] = contestitem['item_id']

        yield item

    def parse(self, response):
        contestitem = {}

        # for item in response.xpath('//div[@class="row"][1]//div[@class="col-md-6"]//div[@class="gtco-icon"]'):
        #     try:
        #         contestitem['item_id'] = self.santize(item.xpath('.//img//@src').get())
        #         # self.item_ids.append(item_id)
        #     except Exception:
        #         pass
        

        for item in response.xpath('//div[@class="row"][1]//div[@class="col-md-6"]//div[@class="gtco-copy"]'):
            try:
                contestitem['item_id'] = self.santize(item.xpath('.//a//@href').get())
                # self.item_ids.append(item_id)
            except Exception as e:
                print("wu")

            try:
                contestitem['name'] = item.xpath('.//h3//text()').get()
                # self.names.append(name)
            except Exception:
                print("wu")
            try:
                link = self.base_url + str(item.xpath('.//a/@href').get())
                
                # crawl landing
                yield scrapy.Request(
                     url=link,
                     callback=self.parse_followed,
                     dont_filter=True,
                     cb_kwargs={'contestitem': contestitem})

            except Exception:
                print("nothing to follow yaaa")
        
        try:
            next_page = str(response.xpath('//div[@class="row"][2]//a[contains(.,"Next Page")]/@href').get())
            if next_page:
                yield scrapy.Request(
                        url=next_page,
                        callback=self.parse,
                        dont_filter=True)
        except Exception:
            print("no next page yaaaa")

        



