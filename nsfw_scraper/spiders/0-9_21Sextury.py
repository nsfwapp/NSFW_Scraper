from scrapy import Spider
import re
import json
from ..items import sceneItem
import scrapy
from datetime import datetime
from selenium import webdriver
from scrapy.contracts import Contract
import time
from scrapy_selenium import SeleniumRequest

base_uri = "https://www.21sextury.com"

#class WithSelenium(Contract):
#        """ Contract to set the request class to be SeleniumRequest for the current call back method to test
#        @with_selenium
#        """
#        name = 'with_selenium'
#        request_cls = SeleniumRequest

class t21SexturySpider(Spider):
    name = "21sextury"
    allowed_domains = ["21sextury.com"]
    custom_settings = {
        'ITEM_PIPELINES': {'nsfw_scraper.pipelines.ScenePipeline': 400},
        'HTTPCACHE_ENABLED' : True,
        'DOWNLOADER_MIDDLEWARES' :
            {
                'scrapy_selenium.SeleniumMiddleware': 300,
                'nsfw_scraper.middlewares.UserAgentRotatorMiddleware': 400,
            }
        }
    start_urls = [
        "https://www.21sextury.com/en/videos"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)


    def parse(self, response):
        #print(response.text)
        scenes = response.xpath("//a[@class=' Link styles_14vPrCCVto Link styles_14vPrCCVto']/@href").getall()
        print(scenes[0])
        
        #for scene_url in range(3):# scenes:
        yield SeleniumRequest(url=base_uri + scenes[0], callback=self.parse_scene)
        #time.sleep(0.5)
        #last_page_url = response.xpath("//div[@data-item='c-51 r-11 t-c-31 / middle right']/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        #for page_num in range(1, 2):
            #yield SeleniumRequest(url=f"https://www.21sextury.com/en/videos?page={page_num}&configure%5BfacetingAfterDistinct%5D=true&configure%5BhitsPerPage%5D=60", callback=self.parse)


    def parse_scene(self, response):

            

            item = sceneItem()
            item['parent_studio'] = '21 Sextury'

            item['title'] = response.selector.xpath("//a[@class='sceneLink  ']/@title").get()
            item['thumbnail_url'] = response.selector.xpath("//video[@class='vjs-tech']/@poster").get()
            item['preview_url'] = response.selector.xpath("//video[@class='vjs-tech']/@src").get()
            item['length'] = ''
            item['description'] = response.xpath("//div[@class='Raw Paragraph SceneDescription-Paragraph styles_14GWIxqGnS styles_1y8nHtPCCl']/text()").get()
            item['gallary_urls'] = ''
            item['studio'] = response.xpath("//a[@class=' Link ScenePlayer-ChannelName-Link undefined-Link Link ScenePlayer-ChannelName-Link undefined-Link']/@title").get()
            item['performers'] = response.xpath("//div[@class='component-ActorThumb-List']/a/@title").getall()
            item['director'] = ''
            item['release_date'] = datetime.strptime(response.xpath("//span[@class='Text ScenePlayer-ReleaseDate-Text styles_3tU3Z2sLeO']/text()").get(), "%Y-%m-%d")
            item['rating'] = ''
            item['movie'] = ''
            item['tags'] = response.xpath("//div[@class='BackgroundBox ScenePlayer-SceneCategories-BackgroundBox styles_1khKtnnA8W']/a/text()").getall()


            yield item
