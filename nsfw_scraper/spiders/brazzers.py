from scrapy import Spider
import re
import json
from ..items import vixenScene
import scrapy
from datetime import datetime
import time

base_uri = "https://brazzers.com"

class BrazzersSpider(Spider):
    name = "brazzers"
    allowed_domains = ["brazzers.com"]
    start_urls = [
        "https://brazzers.com/videos"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@class='dtkdna-4 kBlepe dtkdna-8 dcHfjj']/div/span/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        last_page_url = response.xpath("//li[@class='sowzbh-1 gjRQwQ'][9]/a/@href").get()
        page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://www.brazzers.com/videos/page/{page_num}", callback=self.parse)


    def parse_scene(self, response):

        data = response.xpath("//script[@data-rh='true'][2]/text()").get()
        jsondata = json.loads(data)
        gallary_tmp = []        

        item = vixenScene()

        item['studio'] = response.xpath("//div[@class='vdkjux-3 fRnfXb']/a/text()").get()
        item['parent_studio'] = 'Brazzers'
        item['title'] = jsondata['name']
        item['thumbnail_url'] = jsondata['thumbnailUrl']
        item['preview_url'] = jsondata['contentUrl']       
        item['performers'] = response.xpath("//div[@class='sc-1b6bgon-4 fxEwWY']/span/a/text()").getall()
        item['director'] = ''
        item['length'] = ''
        item['description'] = jsondata['description']
        item['release_date'] = datetime.strptime(response.xpath("//div[@class='sc-1b6bgon-1 jZtBDX']/text()").get(), '%B %d, %Y')
        item['rating_native'] = float(int(response.xpath("//div[@class='sc-1b6bgon-5 dHcveS']/span[1]/text()").get().strip('%'))/10)

        for i in jsondata['page']['data'][scene_path]['data']['pictureset']:
            gallary_tmp.append(i['main'][0]['src'])

        item['gallary_urls'] = gallary_tmp


        yield item
