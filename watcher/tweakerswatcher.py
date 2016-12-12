import requests
import json
import os.path

from watcher.watcher import Watcher

class TweakersWatcher(Watcher):
    watcher_name = 'Tweakers Pricewatch'
    filename = 'site_tweakers.txt'

    def parse_site(self):
        url = 'https://tweakers.net/xmlhttp/xmlHttp.php?application=tweakbase&type=filter&action=deals&dayOffset=1&minRelativePriceDrop=0.4&maxRelativePriceDrop=1&minAbsolutePriceDrop=30&maxAbsolutePriceDrop=&minCurrentPrice=0&maxCurrentPrice=&minPrices=3&minViews=0&of=absolutePriceDrop&od=desc&output=json'
        request = requests.get(url)
        json_object = json.loads(request.text)
        return json_object['data']['html']


    def check_price_error(self):
        url = 'https://tweakers.net/pricewatch/deals/#filter:q1ZKSaz0T0srTi1RsjLUUcpNrAhKzUksySxLDSjKTE51KcovgEhk5jkmFefnlJYgSxgbgGWcS4uKUvNKwBJKVhAxMKcYqATMw2KogZ4JWCosM7W8GKwrvygltcgtMzUnRclKKRHDtloA'
        message_text = 'Mogelijke prijsfout, check: {0}'.format(url)
        html = self.parse_site()

        if not os.path.isfile(self.filename):
            self.write_to_file(self.filename, html)
            exit(0)
        else:
            with open(self.filename, 'r') as f:
                file_content = f.read()
                if file_content != html:
                    self.send_telegram(self.watcher_name, message_text)
            self.write_to_file(self.filename, html)
