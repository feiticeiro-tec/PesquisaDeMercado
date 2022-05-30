import scrapy
from ..get_request import cature_json
from pprint import pprint

class ExtraSpider(scrapy.Spider):
    name = 'extra'
    allowed_domains = ['www.extra.com.br']
    def start_requests(self):
        buscar = getattr(self,'buscar',None)
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host':'www.extra.com.br'}

        if buscar:
            buscar = '-'.join(buscar.split())
        else:
            raise KeyError('Busca não expecificada!')
        yield scrapy.Request(url=f'http://www.extra.com.br/{buscar}/b',callback=self.parse,headers=headers)

    def parse(self, response):
        ids = ','.join(li.attrib['data-cy'].replace('product','') for li in response.css('ul.eFvtpO').css('li'))
        npreço = cature_json('https://npreco.api-extra.com.br/Produtos/PrecoVenda/?idsproduto=',ids,'www.extra.com.br')['PrecoProdutos']
        for index, row in enumerate(response.css('ul.eFvtpO').css('li')):
            nome = row.css('h2::text').get()
            preço = npreço[index]['PrecoVenda']['Preco']
            url = row.css('a').attrib['href']
            image = row.css('img').attrib['src']
            yield {'nome':nome,'preço':preço,'url':url,'image':image}
            
