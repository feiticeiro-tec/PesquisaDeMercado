import scrapy
from ..get_request import cature_html,cature_json
import tempfile


class SubmarinoSpider(scrapy.Spider):
    name = 'submarino'
    allowed_domains = ['www.submarino.com.br']
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
        'Referer':'https://www.submarino.com.br/'}

        html = cature_html(f'https://www.submarino.com.br/busca/{buscar}',headers)
        self.file = tempfile.NamedTemporaryFile('w')
        self.file.write(html)
        yield scrapy.Request(url=f'file://{self.file.name}',callback=self.parse)

    def parse(self, response):
        for row in response.css('div.inStockCard__Wrapper-sc-4ayj0x-0'):
            nome = row.css('h3::text').get()
            preço = float(row.css('span.price__PromotionalPrice-sc-1icb1x-1::text').get().replace('R$','').replace('.','').replace(',','.'))
            image = row.css('img').attrib['src']
            url = 'https://www.submarino.com.br'+row.css('a').attrib['href']
            yield {'nome':nome,'preço':preço,'url':url,'image':image}
