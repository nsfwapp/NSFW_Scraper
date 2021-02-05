from scrapy import Spider
import re
import json
from ..items import sceneItem
import scrapy
from datetime import datetime
import time

base_uri = "https://letsdoeit.com/"

class NameSpider(Spider):
    name = "name"
    allowed_domains = ["letsdoeit.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.ScenePipeline': 400}}
    start_urls = [
        "https://letsdoeit.com/videos.en.html"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@data-item='c-12 r-21']/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        #time.sleep(0.5)
        last_page_url = response.xpath("//div[@data-item='c-51 r-11 t-c-31 / middle right']/a/@href").get()
        page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://letsdoeit.com/videos.en.html?page={page_num}", callback=self.parse)


    def parse_scene(self, response):

            item = sceneItem()

            item['title'] = response.xpath("//h1/text()").get()
            item['thumbnail_url'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='thumbnailUrl']/@content").get()
            item['preview_url'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='contentURL']/@content").get()
            item['length'] = datetime.strptime(' '.join(i for i in re.findall("\d+", response.xpath("//div[@itemprop='video']/meta[@itemprop='duration']/@content").get())),"%M %S").time()
            item['description'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='description']/@content").get()
            item['gallary_urls'] = response.xpath("//div[@class='swiper-slide gallery-swiper-slide']/a/svg/@data-bg").getall()
            item['studio'] = response.xpath("//h2/a/strong/text()").get()
            item['performers'] = response.xpath("//div[@class='actors']/h2/span/a/strong/text()").getall()
            item['director'] = ''
            item['release_date'] = datetime.strptime(response.xpath("//div[@itemprop='video']/meta[@itemprop='uploadDate']/@content").get().split('T')[0], "%Y-%m-%d")
            item['rating'] = ''
            item['movie'] = ''
            item['tags'] = response.xpath("//div[@class='h5 no-space color-rgba255-06']/a/text()").getall()


            yield item
