import scrapy
from requests_html import HTMLSession
from ..get_request import cature_html,cature_json
import os
import tempfile

class CasasBahiaSpider(scrapy.Spider):
    name = 'casas_bahia'
    allowed_domains = ['www.casasbahia.com.br']
    pasta = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    def start_requests(self):
        buscar = getattr(self,'buscar',None)
        if buscar:
            buscar = '+'.join(buscar.split())
        else:
            raise KeyError('Busca não expecificada!')
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.casasbahia.com.br'}

        html = cature_html(f'https://www.casasbahia.com.br/{buscar}/b',headers)
        self.file = tempfile.NamedTemporaryFile('w')
        self.file.write(html)

        yield scrapy.Request(url=f'file://{self.file.name}',callback=self.parse)

    def parse(self, response):
        self.file.close()
        data = []
        for row in response.css('li.ProductCard__Wrapper-sc-2vuvzo-9'):
            Id = row.attrib['data-cy'].replace('product','')
            nome = row.css('h2::text').get()
            url = row.css('a').attrib['href']
            image = row.css('img').attrib['src']
            data.append({'id':Id,'nome':nome,'preço':None,'url':url,'image':image})
        ids = ','.join([i['id'] for i in data])
        npreço = cature_json('https://npreco.api-casasbahia.com.br/Produtos/PrecoVenda/?idsproduto=',ids,'https://www.casasbahia.com.br')['PrecoProdutos']
        for index,row in enumerate(data):
            try:
                row.pop('id')
                row['preço'] = npreço[index]['PrecoVenda']['Preco']
                yield row
            except:
                ...