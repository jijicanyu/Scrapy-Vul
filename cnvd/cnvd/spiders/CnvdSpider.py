# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from cnvd.items import CnvdItem

class Myspider2Spider(scrapy.Spider):
    name = "cnvd"
    allowed_domains = ["www.cnvd.org.cn"]
    # start_urls = ["http://www.exploitalert.com/index.html?page=%d&" % i for i in xrange(1,2)]

    start_urls = [
        'http://www.cnvd.org.cn/flaw/list.htm?field=&startDate=&flag=%5BLjava.lang.String%3B%40b611c5b&max=20&order=&number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&endDate=&offset='+str(i) for i in xrange(1,200,20)
    ]

    def parse(self, response):
        sels = Selector(response).xpath('//tbody/tr')

        for sel in sels:
            # print sel.xpath('td[1]/a/@title').extract_first()
            url = sel.xpath('td[1]/a/@href').extract_first()
            print url
            yield Request(
                    url='http://www.cnvd.org.cn' + url,
                    callback=self.parse_item
                )

    def parse_item(self, response):
        sels = Selector(response)
        item = CnvdItem()
        item['title'] = sels.xpath('//h1/text()').extract_first()
        item['url'] = response.url
        item['snapshot'] = Selector(response).xpath('//*').extract_first()
        count=1
        # path_str ='//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[2]/text()'
        head = sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[1]/text()').extract_first()
        print head
        print type(head)
        # while  not  head==[] :
        while count<=20:
            pass
            # pass
            # str(head)
            temparr=sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[2]/text()').extract()
            body = " ".join([i.strip() for i in temparr])
            # print '-------head------' + body
            if head == 'CNVD-ID':
                item['CNVD_ID']=body
            if head == u'发布时间':
                item['product_date']=body

            if head == u'危害级别':
                print '-----insert level---'
                item['level']=sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[2]').extract_first().replace('<td class="denle">','').replace('<span class="yellow showInfo"></span>','').replace('</td>','').replace('(<a href="#showDiv" class="showInfo">','').replace('</a>)','').replace('<span class="red showInfo"></span>','').replace('<span class="green showInfo"></span>','').strip()
            
            if head == u'影响产品':
                item['effect_production']=body
            if head == u'BUGTRAQ ID':
                item['bugtraq_id']=body
            if head == u'漏洞描述':
                item['cave_desc']=body
            if head == u'参考链接':
                # item['look_link']=body
                temparr=sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[2]/a/text()').extract()
                item['look_link'] = " ".join([i.strip() for i in temparr])
            if head == u'漏洞解决方案':
                item['means']=body
            if head == u'漏洞发现者':
                item['auther']=body
            if head == u'厂商补丁':
                # item['buding']=body
                item['buding'] =sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[2]/a/text()').extract_first()
            if head == u'验证信息':
                item['pinfo']=body
            if head == u'报送时间':
                item['report_date']=body
            if head == u'收录时间':
                item['collect_date']=body
            if head == u'更新时间':
                item['update_date']=body
            if head == u'漏洞附件':
                item['cave_flie']=body
            if head == u'其他 ID':
                item['else_id']=body
            count=count+1
            head = sels.xpath('//table[@class="gg_detail"]/tbody/tr['+str(count)+']/td[1]/text()').extract_first()


        print '-------item------' + item['CNVD_ID']
        print '---------item level----' + item['level']

        #-----------------------------------------------------------------------------------
        # print '-----------url----------'
        # print response.url
        # print '------------content---------'
        # print response.body
        # print '----------end body---------'
        # sels = Selector(response)
        # item = CnvdItem()
        # item['title'] = sels.xpath('//h1/text()').extract_first()
        # item['CNVD_ID']= sels.xpath('//table[@class="gg_detail"]/tbody/tr[1]/td[2]/text()').extract_first()
        # item['product_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[2]/td[2]/text()').extract_first()
        # item['level'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[3]/td[2]/text()[2]').extract_first()
        # #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/text()[1]
        # item['effect_production'] =" ".join(sels.xpath('//table[@class="gg_detail"]/tbody/tr[4]/td[2]/text()').extract_first())
        # #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[4]/td[2]/text()
        # item['bugtraq_id'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[5]/td[2]/a/text()').extract_first()
        # #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[5]/td[2]/a
        
        # temp=sels.xpath('//table[@class="gg_detail"]/tbody/tr[6]/td[1]/text()').extract_first()
        # #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[6]/td[1]
        # if(temp=='CVE ID'):
        #     item['CVE_ID'] = temp
        #     temparr=sels.xpath('//table[@class="gg_detail"]/tbody/tr[7]/td[2]/text()').extract()
        #     print '---------des-------'
        #     for i in temparr:
        #         print i 
        #     item['cave_desc'] = " ".join([i.strip() for i in temparr])
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[6]/td[2]/text()[1]
        #     item['look_link'] =sels.xpath('//table[@class="gg_detail"]/tbody/tr[8]/td[2]/a/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[7]/td[2]/a
        #     item['means'] = " ".join(sels.xpath('//table[@class="gg_detail"]/tbody/tr[9]/td[2]/text()').extract_first())
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[8]/td[2]
        #     item['auther'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[10]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[9]/td[2]
        #     item['buding'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[11]/td[2]/a/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[10]/td[2]/a
        #     item['pinfo'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[12]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[11]/td[2]
        #     item['report_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[13]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[12]/td[2]
        #     item['collect_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[14]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[13]/td[2]
        #     item['update_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[15]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[14]/td[2]
        #     item['cave_flie'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[16]/td[2]/text()').extract_first()
        #     item['url'] = response.url
        #     item['snapshot'] = Selector(response).xpath('//*').extract_first()

        # else:
        #     # the before code 

        #     #item['cave_desc'] = " ".join(sels.xpath('//table[@class="gg_detail"]/tbody/tr[6]/td[2]/text()').extract_first())
        #     temparr=sels.xpath('//table[@class="gg_detail"]/tbody/tr[6]/td[2]/text()').extract()
        #     print '---------des-------'
        #     for i in temparr:
        #         print i 
        #     item['cave_desc'] = " ".join([i.strip() for i in temparr])
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[6]/td[2]/text()[1]
        #     item['look_link'] =sels.xpath('//table[@class="gg_detail"]/tbody/tr[7]/td[2]/a/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[7]/td[2]/a
        #     item['means'] = " ".join(sels.xpath('//table[@class="gg_detail"]/tbody/tr[8]/td[2]/text()').extract_first())
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[8]/td[2]
        #     item['auther'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[9]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[9]/td[2]
        #     item['buding'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[10]/td[2]/a/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[10]/td[2]/a
        #     item['pinfo'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[11]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[11]/td[2]
        #     item['report_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[12]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[12]/td[2]
        #     item['collect_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[13]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[13]/td[2]
        #     item['update_date'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[14]/td[2]/text()').extract_first()
        #     #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[14]/td[2]
        #     item['cave_flie'] = sels.xpath('//table[@class="gg_detail"]/tbody/tr[15]/td[2]/text()').extract_first()
        #     item['url'] = response.url
        #     item['snapshot'] = Selector(response).xpath('//*').extract_first()
        #-------------------------------------------------------------------------------------
        yield item
 