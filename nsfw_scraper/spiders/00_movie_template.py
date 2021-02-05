from scrapy import Spider
import re
import json
from ..items import movieItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.adultdvdempire.com"

class movieSpider(Spider):
    name = "yourspider"
    allowed_domains = ["adultdvdempire.com"]
    custom_settings = {'ITEM_PIPELINES': {'nsfw_scraper.pipelines.MoviePipeline': 400}}
    start_urls = [
        "https://www.adultdvdempire.com/95898/studio/2020-vision-porn-movies.html"
    ]

    def parse(self, response):
        movies = response.xpath("//div[@class='boxcover-container']/a/@href").getall()
        
        for movie_url in movies:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + movie_url, callback=self.parse_scene)
        #time.sleep(0.5)
        next_page_url = response.xpath("//a[@title='Next']/@href").get()
        if next_page_url is not None:
            yield scrapy.Request(url=base_uri + next_page_url, callback=self.parse)


    def parse_scene(self, response):

            item = movieItem()

            item['movie_title'] = response.xpath("//h1/text()").get()
            item['movie_cover'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='thumbnailUrl']/@content").get()
            item['movie_trailer'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='contentURL']/@content").get()
            item['length'] = datetime.strptime(' '.join(i for i in re.findall("\d+", response.xpath("//div[@itemprop='video']/meta[@itemprop='duration']/@content").get())),"%M %S").time()
            item['description'] = response.xpath("//div[@itemprop='video']/meta[@itemprop='description']/@content").get()
            item['gallary_urls'] = response.xpath("//div[@class='swiper-slide gallery-swiper-slide']/a/svg/@data-bg").getall()
            item['studio'] = response.xpath("//h2/a/strong/text()").get()
            item['performers'] = response.xpath("//div[@class='actors']/h2/span/a/strong/text()").getall()
            item['director'] = ''
            item['release_date'] = datetime.strptime(response.xpath("//div[@itemprop='video']/meta[@itemprop='uploadDate']/@content").get().split('T')[0], "%Y-%m-%d")
            item['rating'] = ''
            item['scenes'] = ''
            item['genres']
            item['tags'] = response.xpath("//div[@class='h5 no-space color-rgba255-06']/a/text()").getall()


            yield item
