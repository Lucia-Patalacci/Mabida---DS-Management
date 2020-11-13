import scrapy
from scrapy.crawler import CrawlerProcess
import os
import re
import datetime
import urllib.request
from bs4 import BeautifulSoup
import shutil
import requests
from urllib.parse import urljoin
import sys

STORAGE_DIR = "ikea_image"

class IkeaSpider(scrapy.Spider):
    name = "Ikea"

    def __init__(self, make=None, *args, **kwargs):
        super(IkeaSpider, self).__init__(*args, **kwargs)
        init_url =['https://www.ikea.com/it/it/catalog/productsaz/8/']
        self.start_urls = init_url
        
    def make_soup(url):
      req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
      html = urllib.request.urlopen(req)
      return BeautifulSoup(html, 'html.parser')

    def get_images(self,url):
     soup = make_soup(url)
     images = [img for img in soup.findAll('img')]
     print (str(len(images)) + " images found.")
     print('Downloading images to current working directory.')
     image_links = [each.get('src') for each in images]
     for each in image_links:
         try:
             filename = each.strip().split('/')[-1].strip()
             src = urljoin(url, each)
             print('Getting: ' + filename)
             response = requests.get(src, stream=True)
             # delay to avoid corrupted previews
             time.sleep(1)
             with open(filename, 'wb') as out_file:
                 shutil.copyfileobj(response.raw, out_file)
         except:
             print('  An error occured. Continuing.')
     print('Done.')

    def parse(self, response):
        if not response.headers.get("Content-Type").startswith(b'text/html'):
            return  #non effettua il parsing se il contenuto non e' text/html
        #filename = os.path.join(STORAGE_DIR, re.sub("\W", "_",response.url) + '.html')
        #print('filename')
        #print(filename)
        
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, 'html.parser')
            #soup = make_soup(url)
            images = [img for img in soup.findAll('img')]
            print (str(len(images)) + " images found.")
            print('Downloading images to current working directory.')
            image_links = [each.get('src') for each in images]
            for each in image_links:
             try:
              filename = each.strip().split('/')[-1].strip()
              src = urljoin(url, each)
              print('Getting: ' + filename)
              response = requests.get(src, stream=True)
              # delay to avoid corrupted previews
              time.sleep(1)
              with open(filename, 'wb') as out_file:
                 shutil.copyfileobj(response.raw, out_file)
             except:
              print('  An error occured. Continuing.')
            print('Done.')
            #if url.startswith('https://www.ikea.com/it/it/catalog'):
                #print(url)
                #yield scrapy.Request(url)


#process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','DEPTH_LIMIT':'4'})
process = CrawlerProcess({'DEPTH_LIMIT':'4'})
process.crawl(IkeaSpider) 
process.start()








