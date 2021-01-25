from scrapy import Spider
import re
import json
from ..items import vixenScene
import scrapy
from datetime import datetime
import time

base_uri = "https://blacked.com"

class BlackedSpider(Spider):
    name = "blacked"
    allowed_domains = ["blacked.com"]
    start_urls = [
        "https://blacked.com/videos"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@class='pb6v16-1 fNpwyc']//div[@class='vrtn0d-0 fdoVgg']//div[@class='sc-1z0w6pb-7 cbiAOI']/a/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        time.sleep(0.5)
        last_page_url = response.xpath("//div[@class='sc-8bfwvf-0 jhtprW']//a[@class='sc-8bfwvf-2 cZoJWe active']/@href").get()
        page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://www.blacked.com/videos?page={page_num}&size=12", callback=self.parse)


    def parse_scene(self, response):

        res = response.text.encode().decode('unicode_escape')
        data = re.search(r'window\.__INITIAL_STATE__ = ({.*});', res).group(1)
        jsondata = json.loads(data)
        scene_path = jsondata['location']['pathname']
        gallary_tmp = []        

        item = vixenScene()

        item['studio'] = 'Blacked'
        item['parent_studio'] = ''
        item['title'] = response.xpath("//*[@id='root']/main/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/h1/text()").get()

        for i in jsondata['videos']:
            if response.xpath("//*[@id='root']/main/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/h1/text()").get() == i['title']:
                item['thumbnail_url'] = i['images']['poster'][-1]['src']
                #item['thumbnail_hd_url'] = i['images']['poster'][-1]['highdpi']['3x']
                item['preview_url'] = i['previews']['poster'][-1]['src']        

        item['performers'] = response.xpath("//div[@data-test-component='VideoModels']/a/text()").getall()
        item['director'] = response.xpath("//span[@data-test-component='DirectorText']/text()").get()
        item['length'] = datetime.strptime(response.xpath("//span[@data-test-component='RunLengthFormatted']/text()").get(), '%M:%S').time()
        item['description'] = response.xpath("//div[@data-test-component='VideoDescription']/div/p/text()").get()
        item['release_date'] = datetime.strptime(response.xpath("//span[@data-test-component='ReleaseDateFormatted']/text()").get(), '%B %d, %Y')
        item['rating_native'] = float(response.xpath("//span[@data-test-component='RatingNumber']/text()").get())

        for i in jsondata['page']['data'][scene_path]['data']['pictureset']:
            gallary_tmp.append(i['main'][0]['src'])

        item['gallary_urls'] = gallary_tmp


        yield item
