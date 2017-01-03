import requests
import json
import os.path
from bs4 import BeautifulSoup

from watcher.watcher import Watcher

class TweakersWatcher(Watcher):
    watcher_name = 'Tweakers Pricewatch'
    filename = 'site_tweakers.txt'

    def parse_site(self):
        url = 'https://tweakers.net/xmlhttp/xmlHttp.php?application=tweakbase&type=filter&action=deals&dayOffset=1&minRelativePriceDrop=0.4&maxRelativePriceDrop=1&minAbsolutePriceDrop=30&maxAbsolutePriceDrop=&minCurrentPrice=0&maxCurrentPrice=&minPrices=3&minViews=0&pageSize=10000&of=absolutePriceDrop&od=desc&output=json'
        request = requests.get(url)
        json_object = json.loads(request.text)
        soup = BeautifulSoup(json_object['data']['html'], 'html.parser')
        product_rows = soup.find_all('a', class_='product')
        product_titles = []
        for product_row in product_rows:
            product_titles.append(product_row['title'])
        return product_titles


    def check_price_error(self):
        url = 'https://tweakers.net/pricewatch/deals/#filter:q1ZKSaz0T0srTi1RsjLUUcpNrAhKzUksySxLDSjKTE51KcovgEhk5jkmFefnlJYgSxgbgGWcS4uKUvNKwBJKVhAxMKcYqATMw2KogZ4JWCosM7W8GKwrvygltcgtMzUnRclKKRHDtloA'
        products = self.parse_site()
        products_string = '\n'.join(products)
        if not os.path.isfile(self.filename):
            self.write_to_file(self.filename, products_string)
            exit(0)
        else:
            with open(self.filename, 'r') as f:
                products_from_file = f.read().split('\n')
                for product in products:
                    if not product in products_from_file:
                        message_text = 'Mogelijke prijsfout, product: {0} , check: {1}'.format(product, url)
                        self.send_telegram(self.watcher_name, message_text)
            self.write_to_file(self.filename, products_string)
