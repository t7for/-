import scrapy
from Douban.items import DoubanItem

class DbSpider(scrapy.Spider):
    name = "db"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):

        #获取列表
        movie_list=response.xpath('//*[@class="info"]')
        for movie in movie_list:
            #实例化DoubanItem
            item=DoubanItem()
            #定义爬取信息
            item['name']=movie.xpath('//div[@class="info"]/div[1]/a/span[1]/text()').extract_first()
            item['info']=movie.xpath('//div[@class="item"]//p[1]/text()[1]').extract_first().strip()
            item['score']=movie.xpath('//div[2]/div[@class="bd"]/div/span[2]/text()').extract_first()
            #拿电影的引言
            item['quote']=movie.xpath('//div[2]/p[@class="quote"]/span/text()').extract_first()

            yield item
        

        url=response.xpath('//span[@class="next"]/a').extract_first()
        if url!=None:
            url=response.urljoin(url)
            yield scrapy.Request(url=url,callback=self.parse)