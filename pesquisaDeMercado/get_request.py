from requests import session
from requests_html import HTMLSession
import json

def cature_html(url,headers):
    session = HTMLSession()
    
    response = session.get(url=url,headers=headers)
    response.html.render(sleep=1)
    return response.text

def cature_json(url,ids,origin):
    session = HTMLSession()
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': origin}
    response = session.get(url=f'{url}{ids}',headers=headers)
    response.html.render(sleep=1)
    return json.loads(response.text)