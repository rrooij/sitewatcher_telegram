import requests
import json
import os.path

from watcher.watcher import Watcher

class BolWatcher(Watcher):
    watcher_name = 'Bol.com'
    filename = 'site_bol.txt'

    def filter_laptop(self, product):
        try:
            if float(product['price']['price']['price']) < 190.0:
                return True
            return False
        except TypeError:
            return False

    def parse_laptop_cat(self):
        url = 'https://www.bol.com/nl/l/ajax/index.html?n=4770+32606&origin=8&page=1&section=computer&sort=PDT_WSP_SORT_PRICE0&bltgc=i-LGZKatR5sesRHShf1H8Q'
        request_json = requests.get(url)
        json_obj = json.loads(request_json.text)
        products = json_obj['itemsContent']['items']
        return products

    def check_price_error(self):
        products = self.parse_laptop_cat()
        products_low_price = [product for product in products if self.filter_laptop(product)]
        products_string = '\n'.join(d['title'] for d in products_low_price)
        if not os.path.isfile(self.filename):
            self.write_to_file(self.filename, products_string)
            exit(0)
        else:
            with open(self.filename, 'r') as f:
                products_from_file = f.read().split('\n')
                products_not_in_file = [x for x in products_low_price if x['title'] not in products_from_file]
                for product in products_not_in_file:
                    url = 'https://www.bol.com'
                    message = 'Mogelijke prijsfout, product: [{0}]({1})\n Prijs: {2}'.format(product['title'], url + product['productPageUrl'], product['price']['price']['price'])
                    print(message)
                    self.send_telegram(self.watcher_name, message)
            self.write_to_file(self.filename, products_string)
