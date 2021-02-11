from scrapy import Spider
from string import ascii_uppercase
import re
import json, logging
from ..items import performerItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.18vr.com"

class _18vrPerformerSpider(Spider):
    name = "18vrPerformer"
    allowed_domains = ["18vr.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.PerformerPipeline': 400}}
    start_urls = [
        "https://18vr.com/vrgirls?order=newest"
    ]
    

    def parse(self, response):

        performers = response.xpath("//div[@class='girl-card-info']/a/@href").getall()

        for performer_url in performers:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + performer_url, callback=self.parse_performer)
        #last_page_url = response.xpath("//li[@class='sowzbh-1 gjRQwQ'][7]/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1,16):
            yield scrapy.Request(url=f"https://18vr.com/vrgirls/{page_num}?order=newest", callback=self.parse)

        


    def parse_performer(self, response):


        item = performerItem()

        item['name'] = response.xpath("//h1/text()").get()

        item['aliases'] = None

        item['gender'] = 'Female'

        item['description'] = response.xpath("//p[@id='girlBio']/text()").get()


        item['profile_pic'] = [response.xpath("//img[@id='girlImage']/@src").get().split('?')[0]]

        item['date_of_birth'] = None # get age from here


        item['years_active'] = None


        item['ethnicity'] = response.xpath("//li[@class='girl-details-stats-item'][7]/span[2]/text()").get()

        item['birth_place'] = response.xpath("//li[@class='girl-details-stats-item'][4]/span[2]/text()").get()


        item['height'] = response.xpath("//li[@class='girl-details-stats-item'][2]/span[2]/text()").get()


        item['hair_color'] = response.xpath("//li[@class='girl-details-stats-item'][5]/span[2]/text()").get()


        item['eye_color'] = response.xpath("//li[@class='girl-details-stats-item'][6]/span[2]/text()").get()

        item['boobs'] = response.xpath("//ul[@id='biolist']/li[13]/a/text()").get()


        item['tattoos'] = None


        item['piercings'] = None

        item['measurments'] = response.xpath("//li[@class='girl-details-stats-item'][1]/span[2]/text()").get()

        item['rating'] = None

        yield item
