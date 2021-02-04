from scrapy import Spider
import re
import json
from ..items import movieItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.adultdvdempire.com"

class sixamstudiosSpider(Spider):
    name = "6amstudios"
    allowed_domains = ["adultdvdempire.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.MoviePipeline': 400}}
    start_urls = [
        "https://www.adultdvdempire.com/95898/studio/2020-vision-porn-movies.html"
    ]

    def parse(self, response):
        movies = response.xpath("//div[@class='boxcover-container']/a/@href").getall()
        
        for movie_url in movies:
            print(base_uri + movie_url.strip())
            yield scrapy.Request(url=base_uri + movie_url.strip(), callback=self.parse_scene)
        #time.sleep(0.5)
        next_page_url = response.xpath("//a[@title='Next']/@href").get()
        if next_page_url is not None:
            yield scrapy.Request(url=base_uri + next_page_url, callback=self.parse)


    def parse_scene(self, response):

            item = movieItem()

            item['movie_title'] = response.xpath("//h1/text()").get().strip()
            item['movie_cover'] = response.xpath("//a[@id='front-cover']/img/@src").get()
            item['movie_trailer'] = '' #todo
            item['length'] = '' #todo datetime.strptime(response.xpath("//ul[@class='list-unstyled m-b-2']/li[1]/text()").get().strip(),"%H hrs. %M mins.").time()
            item['description'] = '' #todo
            item['gallary_urls'] = '' #todo
            item['studio'] = '2020Vision'
            item['performers'] = response.xpath("//div[@class='m-b-1']/a/div/u/text()").getall()

            if response.xpath("//a[@label='Director']/text()").get() is not None:
                item['director'] = response.xpath("//a[@label='Director']/text()").get().strip()
            else:
                item['director'] = ''

            item['release_date'] = datetime.strptime(response.xpath("//ul[@class='list-unstyled m-b-2']/li[3]/text()").get().strip(), "%b %d %Y")
            item['rating'] = ''
            item['scenes'] = ''
            item['genres'] = response.xpath("//div[@class='m-b-1'][3]/a/text()").getall()
            item['tags'] = ''


            yield item
