from scrapy import Spider
import re
import json
from ..items import sceneItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.blowpass.com/en"

class BlackedSpider(Spider):
    name = "blowpass"
    allowed_domains = ["blowpass.com"]
    start_urls = [
        "https://www.blowpass.com/en/videos"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@class='sceneContainer']/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        #time.sleep(0.5)
        last_page_url = response.xpath("//a[@class='last GA GA_Click GA_Id_videosAllpaginator_bottom_PagerLast']/@href").get()
        page_num = re.findall("\d+", last_page_url)[-1]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://www.blowpass.com/en/videos/blowpass/latest/All-Categories/0/All-Pornstars/0/{page_num}", callback=self.parse)


    def parse_scene(self, response):

            prev_base_uri = 'https://trailers-openlife.gammacdn.com/'

            item = sceneItem()

            item['title'] = response.xpath("//meta[@property='og:title']/@content").get()
            item['thumbnail_url'] = response.xpath("//meta[@property='og:image']/@content").get()
            item['preview_url'] = prev_base_uri + response.xpath("//a[@size='4k']/@file").get()

            data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
            len_raw = data[0]['duration']
            item['length'] = datetime.strptime(len_raw, "PT%H:%M:%S").time()
            
            item['description'] = response.xpath("//meta[@property='og:description']/@content").get()
            item['gallary_urls'] = ''
            item['studio'] = response.xpath("//span[@class='siteNameSpan']/text()").get()
            item['performers'] = response.xpath("//span[@class='slide-title']/text()").getall()
            item['director'] = ''
            item['release_date'] = datetime.strptime(response.xpath("//p[@class='updatedDate']/text()").getall()[1].strip(), "%m-%d-%Y")
            item['rating'] = ''
            item['movie'] = ''
            item['tags'] = response.xpath("//div[@class='sceneCategories']/a/text()").getall()


            yield item
