from scrapy import Spider
import re
import json
from ..items import sceneItem
import scrapy
from datetime import datetime
import time

base_uri = "https://18vr.com/"

class vr18Spider(Spider):
    name = "18vr"
    allowed_domains = ["18vr.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.ScenePipeline': 400}}
    start_urls = [
        "https://18vr.com/vrpornvideos"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@class='tile-grid-item']/div/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        #time.sleep(0.5)
        last_page_url = response.xpath("//li[@class='pagination-item']/a/@href").getall()[-1]
        page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://18vr.com/vrpornvideos/{page_num}", callback=self.parse)


    def parse_scene(self, response):

            item = sceneItem()
            item['parent_studio'] = None

            gallary_list = []

            for i in range(len(response.xpath("//div[@class='gallery-image-container']/picture/img/@src").getall())):
                gallary_list.append(response.xpath("//div[@class='gallery-image-container']/picture/img/@src").getall()[i].split(',')[-1].strip().split('?')[0])


            item['title'] = response.xpath("//a/span[@itemprop='name']/text()").getall()[-1]
            item['thumbnail_url'] = response.xpath("//source/@srcset").getall()[0].split(',')[-1].strip().split('?')[0]
            item['preview_url'] = ''
            item['length'] = datetime.strptime(response.xpath("//p[@class='video-duration']/@content").get(),"PT%MM%SS").time()
            item['description'] = response.xpath("//p[@class='video-description']/text()").get()
            item['gallary_urls'] = gallary_list
            item['studio'] = '18vr'
            item['performers'] = response.xpath("//p[@class='video-actors']/a/text()").getall()
            item['director'] = ''
            item['release_date'] = datetime.strptime(response.xpath("//p[@class='video-upload-date']/text()").get().split(':')[1].strip(), '%B %d, %Y').date()
            item['rating'] = ''
            item['movie'] = ''
            item['tags'] = response.xpath("//p[@class='video-tags']/a/text()").getall()


            yield item
