import requests
import json
import os.path

from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution

from watcher.watcher import Watcher

class TweakersWatcher(Watcher):
    watcher_name = 'Tweakers Pricewatch'
    filename = 'site_tweakers.txt'

    def parse_site(self):
        url = 'https://tweakers.net/xmlhttp/xmlHttp.php?application=tweakbase&type=filter&action=deals&dayOffset=1&minRelativePriceDrop=0.4&maxRelativePriceDrop=1&minAbsolutePriceDrop=30&maxAbsolutePriceDrop=&minCurrentPrice=0&maxCurrentPrice=&minPrices=3&minViews=0&pageSize=10000&of=absolutePriceDrop&od=desc&output=json'
        request = requests.get(url)
        json_object = json.loads(request.text)
        soup = BeautifulSoup(json_object['data']['html'], 'html.parser')
        product_rows = soup.find_all('tr')
        products = []
        for product_row in product_rows:
            product_a_tag = product_row.find('a', class_='product')
            product_descr = product_row.find('p', class_='specline').find('a').get_text()
            product = { 'title': product_a_tag['title'], 'descr': product_descr, 'url': product_a_tag['href'] }
            products.append(product)
        return products


    def check_price_error(self):
        url = 'https://tweakers.net/pricewatch/deals/#filter:q1ZKSaz0T0srTi1RsjLUUcpNrAhKzUksySxLDSjKTE51KcovgEhk5jkmFefnlJYgSxgbgGWcS4uKUvNKwBJKVhAxMKcYqATMw2KogZ4JWCosM7W8GKwrvygltcgtMzUnRclKKRHDtloA'
        products = self.parse_site()
        products_string = '\n'.join(d['title'] for d in products)
        if not os.path.isfile(self.filename):
            self.write_to_file(self.filename, products_string)
            exit(0)
        else:
            with open(self.filename, 'r') as f:
                products_from_file = f.read().split('\n')
                for product in products:
                    if not product['title'] in products_from_file:
                        message_text = (
                            'Mogelijke prijsfout, product: [{0}]({1}) , beschrijving: {2} check: {3}'
                            .format(product['title'], product['url'], product['descr'], url)
                        )
                        self.send_telegram(self.watcher_name, message_text)
            self.write_to_file(self.filename, products_string)
