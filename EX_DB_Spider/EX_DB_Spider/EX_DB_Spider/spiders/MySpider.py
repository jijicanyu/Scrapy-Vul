# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from EX_DB_Spider.items import ExDbSpiderItem

class MyspiderSpider(scrapy.Spider):
    name = "exdbs"
    allowed_domains = ["exploit-db.com"]
    start_urls = (
        'https://www.exploit-db.com/webapps/?order_by=date&order=desc&pg=1',
    )

    def parse(self, response):
        sels = Selector(response).xpath('//table/tbody/tr/td[5]/a')

        for sel in sels:
            item = ExDbSpiderItem()
            item['edb_title'] = sel.xpath('text()').extract_first()
            url = sel.xpath('@href').extract_first()

            yield Request(
                url = url,
                callback=self.parse_item,
                meta = {'item': item}
            )

    def parse_item(self, response):
        item = response.meta['item']

        page = Selector(response)

        table = page.xpath('//table[@class="exploit_list"]')

        item['edb_id'] = table.xpath('tr[1]/td[1]/text()').extract_first().strip()
        item['edb_author'] = table.xpath('tr[1]/td[2]/a/text()').extract_first().strip()
        item['edb_cve'] = None
        cve_id = table.re('<td><strong>CVE:</strong> (.+)</td>')[0].strip()
        if 'N/A' not in cve_id:
            cve_id = table.re('<td><strong>CVE:</strong>.*?(\d+-\d+)</a>')[0]
            item['edb_cve'] = "CVE-%s" % cve_id

        item['edb_date'] = table.xpath('tr[2]/td[1]/text()').extract_first().strip()
        item['edb_type'] = table.xpath('tr[2]/td[2]/a/text()').extract_first().strip()
        item['edb_platform'] = table.xpath('tr[2]/td[3]/a/text()').extract_first().strip()
        item['edb_exp'] = page.xpath('//pre/text()').extract_first().strip()
        yield item









