import scrapy
import re
import os
#from urllib.parse import urljoin

STORAGE_DIR = "pages_2018/ikea"

class IkeaSpider(scrapy.Spider) :

    name = "Ikea"
    allower_domains = ["https://www.ikea.com/"]
    start_urls = ["https://www.ikea.com/it/it/catalog/productsaz/8/"]
    
    def parse(self, response):
        
        if not response.headers.get("Content-Type").startswith(b'text/html'):
            print("NOT TEXT")
            return  #non effettua il parsing se il contenuto non e' text/html
        
        filename = os.path.join(STORAGE_DIR, re.sub("\W", "_", response.url) + '.html')
        #filename2 = os.path.join(STORAGE_DIR, re.sub("\W", "_", response.url) + '.html')

        with open(filename, 'wb') as f:
            f.write(response.body)
        
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            if url.startswith("https://www.ikea.com/it/it/catalog"):
                yield scrapy.Request(url)

#da terminale: scrapy runspider ikea_crawl.py -s DEPTH_LIMIT=4