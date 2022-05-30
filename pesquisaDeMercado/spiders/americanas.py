import scrapy
import tempfile
from ..get_request import cature_html,cature_json

class AmericanasSpider(scrapy.Spider):
    name = 'americanas'
    allowed_domains = ['www.americanas.com.br']

    def start_requests(self):
        buscar = getattr(self,'buscar',None)
        if buscar:
            buscar = '-'.join(buscar.split())
        else:
            raise KeyError('Busca não expecificada!')
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'http://www.americanas.com.br'}

        html = cature_html(f'http://www.americanas.com.br/busca/{buscar}',headers)
        self.file = tempfile.NamedTemporaryFile('w')
        self.file.write(html)

        yield scrapy.Request(url=f'file://{self.file.name}',callback=self.parse)


    def parse(self, response):
        self.file.close()
        for row in response.css('div.jGlQWu'):
            nome = row.css('h3::text').get()
            preço = float(row.css('span.price__PromotionalPrice-sc-h6xgft-1::text').get().replace('R$','').replace('.','').replace(',','.'))
            url = 'http://www.americanas.com.br'+row.css('a').attrib['href']
            image = row.css('img').attrib['src']
            yield {'nome':nome,'preço':preço,'url':url,'image':image}