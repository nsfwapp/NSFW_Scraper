from scrapy import Spider
import re
import json
from nsfw_scraper.items import vixenScene
import scrapy
import time

base_uri = "https://vixen.com"

class VixenSpider(Spider):
    name = "vixen"
    allowed_domains = ["vixen.com"]
    start_urls = [
        "https://vixen.com/videos"
    ]

    def parse(self, response):
        scenes = response.xpath("//div[@class='pb6v16-1 fNpwyc']//div[@class='vrtn0d-0 fdoVgg']//div[@class='sc-10d9zl9-0 grTQQq']//div[@class='sc-10d9zl9-1 hkDIew']//a[@class='sc-10d9zl9-2 cqKQGx']/@href").getall()
        
        for scene_url in scenes:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri + scene_url, callback=self.parse_scene)
        time.sleep(3)
        last_page_url = response.xpath("//div[@class='sc-8bfwvf-0 jhtprW']//a[@class='sc-8bfwvf-2 cZoJWe active']/@href").get()
        page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1, int(page_num)+1):
            yield scrapy.Request(url=f"https://www.vixen.com/videos?page={page_num}&size=12", callback=self.parse)


    def parse_scene(self, response):

        res = response.text.encode().decode('unicode_escape')
        data = re.search(r'window\.__INITIAL_STATE__ = ({.*});', res).group(1)
        jsondata = json.loads(data)
        scene_path = jsondata['location']['pathname']
        gallary_tmp = []        

        item = vixenScene()

        item['studio'] = 'Vixen'
        item['sub_studio'] = 'None'
        item['name'] = response.xpath("//*[@id='root']/main/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/h1/text()").get()

        for i in jsondata['videos']:
            if response.xpath("//*[@id='root']/main/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/h1/text()").get() == i['title']:
                item['thumbnail_url'] = i['images']['poster'][-1]['src']
                item['thumbnail_hd_url'] = i['images']['poster'][-1]['highdpi']['3x']
                item['preview_url'] = i['previews']['poster'][-1]['src']        

        item['performers'] = response.xpath("//div[@data-test-component='VideoModels']/a/text()").getall()
        item['director'] = response.xpath("//span[@data-test-component='DirectorText']/text()").get()
        item['length'] = response.xpath("//span[@data-test-component='RunLengthFormatted']/text()").get()
        item['description'] = response.xpath("//div[@data-test-component='VideoDescription']/div/p/text()").get()
        item['release_date'] = response.xpath("//span[@data-test-component='ReleaseDateFormatted']/text()").get()
        item['rating_native'] = response.xpath("//span[@data-test-component='RatingNumber']/text()").get()

        for i in jsondata['page']['data'][scene_path]['data']['pictureset']:
            gallary_tmp.append(i['main'][0]['src'])

        item['gallary_urls'] = gallary_tmp


        yield item
