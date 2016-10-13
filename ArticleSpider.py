# -*- coding: utf-8 -*-

#sovle the encode of chinese
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="glyang"
__mtime__ = '2016/10/9  10:39'
"""
import scrapy
from scrapy.selector import Selector

class ArtileSpider(scrapy.Spider):
    '''
    to create a Spider, you need extends form scrapy.Spider object, and define following three attributes and methods:
    name: id
    start_urls
    parse()
    '''
    name = "article"
    #allowed_domains = ["aint-bad.com"]
    allowed_domains = ["featureshoot.com"]
    start_urls = (
        'http://www.featureshoot.com/',
    )

    #http: // www.featureshoot.com / tag / best /
    #http: // www.featureshoot.com / tag / fine - art - photography /
    '''
    def parse(self, response):
        link = 'http://www.featureshoot.com/tag/best/page/'
        for index in xrange(5):
            yield scrapy.Request(link+str(index+1), callback=self.parseSubclass)
        #yield scrapy.Request(link, callback=self.parseSubclass)
    '''
    #解析网站主页
    def parse(self,response):
        link = 'http://www.featureshoot.com'
        yield scrapy.Request(link, self.parseSubclassMain)
    #从主页信息提取出各个模块链接
    def parseSubclassMain(self, response):
        sel = Selector(response)
        # 首页模块
        mainClass = sel.xpath('//div[@id="header"]//ul/li/a')
        Mainlink = []
        for sub in mainClass:
            Mainlink.append(sub.xpath('@href').extract()[0])
        Mainlink.remove('#')
        print Mainlink
        for sub1 in Mainlink:
            for index in xrange(10):
                #每个子模块爬多少页
                yield scrapy.Request(sub1 + 'page/' + str(index + 1), callback=self.parseSubclass)
        '''
        #其他模块
        subClass = sel.xpath('//ul/li/ul/li/a')
        for sub in subClass:
            otherlink = sub.xpath('@href').extract()[0]
            print otherlink
            for index in xrange(1):
                # 每个子模块爬2页
                yield scrapy.Request(otherlink + 'page/' + str(index + 1), callback=self.parseSubclass)
        '''
    #解析模块网页里的文章（文章名字跟链接）
    def parseSubclass(self, response):
        sel = Selector(response)
        subClass = sel.xpath('//*[@class="title"]/a')
        for sub in subClass:
            name = sub.xpath('text()').extract()[0]
            link = sub.xpath('@href').extract()[0]
            print name,link
            yield scrapy.Request(link, callback=self.parseContent,meta={'name':name})
    #解析文章内容，存储文件中
    def parseContent(self, response):
        filename = response.meta['name']
        fileClass = open(filename+".txt",'w')
        content = ''
        sel = Selector(response)
        detai = sel.xpath('//*[@class="content"]/p//text()').extract()
        for con in detai:
            content += con + '\n'
        fileClass.write(content)
        fileClass.flush()
        fileClass.close()





