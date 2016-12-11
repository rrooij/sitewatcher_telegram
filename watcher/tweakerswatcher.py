import requests
import json
import os.path

from watcher.watcher import Watcher

class TweakersWatcher(Watcher):
    watcher_name = 'Tweakers Pricewatch'
    filename = 'site_tweakers.txt'

    def parse_site(self):
        url = 'https://tweakers.net/xmlhttp/xmlHttp.php?application=tweakbase&type=filter&action=deals&fromHash=1&currFilters=q1ZKSaz0T0srTi1RsjLUUcpNrAhKzUksySxLDSjKTE51KcovgEhk5jkmFefnlJYgSxgZgGWcS4uKUvNKwBJKVhAxMKcYpheLoQZ6ZmCpsMzUcqA6g1oA&output=json';
        request = requests.get(url)
        json_object = json.loads(request.text)
        return json_object['data']['html']


    def check_price_error(self):
        url = 'https://tweakers.net/pricewatch/deals/#filter:q1ZKSaz0T0srTi1RsjLUUcpNrAhKzUksySxLDSjKTE51KcovgEhk5jkmFefnlJYgSxgZgGWcS4uKUvNKwBJKVhAxMKcYpheLoQZ6ZmCpsMzUcqA6g1oA'
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
