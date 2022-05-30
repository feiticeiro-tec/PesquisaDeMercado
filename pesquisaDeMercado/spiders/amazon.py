import scrapy
import json
from random import choice

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com.br']
    
    def start_requests(self):
        url = 'https://www.amazon.com.br/s?k='
        buscar = getattr(self,'buscar',None)
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.amazon.com.br'}
        if buscar:
            url += '+'.join(buscar.split())
        else:
            raise KeyError('Busca não expecificada!')
        yield scrapy.Request(url=url,callback=self.parse,headers=headers)

    def parse(self, response):
        lista = response.css('div.s-card-container')
        
        for row in lista:
            try:
                url = 'https://www.amazon.com.br'+row.css('h2').css('a').attrib['href']
                nome = row.css('h2 ::text').get().strip()
                preço = float(row.css('span.a-offscreen::text').get().replace('R$','').strip().replace('.','').replace(',','.'))
                image = row.css('img').attrib['src']
                yield {'nome':nome,'preço':preço,'url':url,'image':image}
            except:
                ...
    