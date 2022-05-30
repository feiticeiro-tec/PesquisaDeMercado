from requests import request
from scrapy.crawler import CrawlerProcess
from pesquisaDeMercado.spiders import *
import subprocess
from flask import current_app,jsonify,render_template,request
import json
from pandas import DataFrame
from random import randint
import os

app = current_app
def run_crawl(buscar):
    data = []
    nome = ''.join([str(randint(1,10)) for i in range(10)])+'.json'
    for loja in ['amazon','americanas','casas_bahia','extra','submarino']:
        subprocess.run(['heroku','run','scrapy','crawl',loja,'-a',f'buscar="{buscar}"','-O',nome,'--app','pesquisa-de-mercado-python'])
        with open(nome) as file:
            for row in json.loads(file.read()):
                data.append(row)
    os.remove(nome)
    return data

@app.route('/')
def index():
    buscar = request.args.get('buscar',None)
    if buscar:
        df = DataFrame(run_crawl(buscar))
        df = df.sort_values(['preço'])
        data = json.loads(df.to_json())
        return render_template('index.html',data=data)
    return render_template('index.html')