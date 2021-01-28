from scrapy import Spider
import re
import json, logging
from ..items import performerItem
import scrapy
from datetime import datetime
import time

base_uri = "https://brazzers.com"

class BrazzersPerformerSpider(Spider):
    name = "brazzersPerformer"
    allowed_domains = ["brazzers.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.PerformerPipeline': 400}}
    start_urls = [
        "https://brazzers.com/pornstars"
    ]
    

    def parse(self, response):
        scenes = response.xpath("//div[@class='dtkdna-1 hfdegr']/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        #last_page_url = response.xpath("//li[@class='sowzbh-1 gjRQwQ'][7]/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, 78):
            yield scrapy.Request(url=f"https://www.brazzers.com/pornstars/page/{page_num}", callback=self.parse)


    def parse_scene(self, response):

        item = performerItem()

        item['name'] = response.xpath("//div[@class='ebvhsz-1 dxRULB font-secondary']/text()").get()
        item['profile_pic'] = response.xpath("//img[@class='syf9gw-1 fZSTdE']/@src").get()      
        item['description'] = response.xpath("//p[@class='xnzhm0-1 jlxcEX']/text()").get()
        item['date_of_birth'] = response.xpath("//li[1]/span[2]/text()").get()
        item['birth_place'] = response.xpath("//li[2]/span[2]/text()").get()
        item['height'] = response.xpath("//li[3]/span[2]/text()").get()
        item['measurments'] = response.xpath("//li[4]/span[2]/text()").get()

        yield item
