from scrapy import Spider
from string import ascii_uppercase
import re
import json, logging
from ..items import performerItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.babepedia.com"

class AD4XPerformerSpider(Spider):
    name = "ad4xPerformer"
    allowed_domains = ["ad4x.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.PerformerPipeline': 400}}
    start_urls = [
        "https://ad4x.com/tour/en/models/all"
    ]
    

    def parse(self, response):

        performers = response.xpath("//div[@class='inner-wrap']/a/img/@src").getall()

        for performer_url in performers:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=performer_url, callback=self.parse_performer)
        #last_page_url = response.xpath("//li[@class='sowzbh-1 gjRQwQ'][7]/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1,14):
            yield scrapy.Request(url=f"https://ad4x.com/tour/en/models/all?page={page_num}", callback=self.parse)

        


    def parse_performer(self, response):

        atr = response.xpath("//li/span/text()").getall() # bio fiels available

        item = performerItem()

        item['name'] = response.xpath("//h2[@class='mb-4 model-name']/font/font/text()").get()

        if response.xpath("//h2[@id='aka']/text()").get() is not None:
            item['aliases'] = response.xpath("//h2[@id='aka']/text()").get()
        else:
            item['aliases'] = ''

        item['gender'] = 'Female'

        if response.xpath("//div[@class='babebanner separate']/p/text()").getall() == []:
            item['description'] = ''
        else:
            lines = response.xpath("//div[@class='babebanner separate']/p/text()").getall()
            description = ''.join(line for line in lines)
            description = description.replace("\n","")
            item['description'] = description

        item['profile_pic'] = [base_uri + response.xpath("//div[@id='profimg']/a/@href").get()]

        date_list = response.xpath("//ul[@id='biolist']/li[2]/a/text()").getall()
        d1s = date_list[0].split(' ')
        d1s[0] = re.findall("\d+", d1s[0])[0]
        d1s = ' '.join(i for i in d1s)
        date_list[0] = d1s
        full_date = ' '.join(i for i in date_list)
        item['date_of_birth'] = datetime.strptime(full_date, '%d of %B %Y') # get age from here

        if "Years active:" in atr:
            item['years_active'] = response.xpath("//ul[@id='biolist']/li[14]/text()").get()
        else:
            item['years_active'] = ''

        if response.xpath("//ul[@id='biolist']/li[4]/a/text()").get() is not None:
            item['ethnicity'] = response.xpath("//ul[@id='biolist']/li[4]/a/text()").get()
        else:
            item['ethnicity'] = response.xpath("//ul[@id='biolist']/li[4]/text()").get()

        item['birth_place'] = response.xpath("//ul[@id='biolist']/li[3]/a/text()").get().strip()

        height = response.xpath("//ul[@id='biolist']/li[8]/text()").get().strip()
        height_in_cm = re.findall("\d+", height)[2]
        item['height'] = height_in_cm

        if response.xpath("//ul[@id='biolist']/li[6]/a/text()").get() is not None:
            item['hair_color'] = response.xpath("//ul[@id='biolist']/li[6]/a/text()").get()
        else:
            item['hair_color'] = response.xpath("//ul[@id='biolist']/li[6]/text()").get()

        if response.xpath("//ul[@id='biolist']/li[7]/a/text()").get() is not None:
            item['eye_color'] = response.xpath("//ul[@id='biolist']/li[7]/a/text()").get()
        else:
            item['eye_color'] = response.xpath("//ul[@id='biolist']/li[7]/text()").get().strip()

        item['boobs'] = response.xpath("//ul[@id='biolist']/li[13]/a/text()").get()

        if "Tattoos:" in atr:
            item['tattoos'] = response.xpath("//ul[@id='biolist']/li[15]/text()").get()
        else:
            item['tattoos'] = ''

        if "Piercings:" in atr and "Tattoos:" in atr:
            item['piercings'] = response.xpath("//ul[@id='biolist']/li[16]/text()").get()
        elif "Piercings:" in atr and "Tattoos:" not in atr:
            item['piercings'] = response.xpath("//ul[@id='biolist']/li[15]/text()").get()
        else:
            item['piercings'] = ''

        item['measurments'] = response.xpath("//ul[@id='biolist']/li[11]/text()").get().strip()

        item['rating'] = round(float(response.xpath("//div[@class='general rating']/b/text()").get().split('/')[0]), 1)

        yield item
