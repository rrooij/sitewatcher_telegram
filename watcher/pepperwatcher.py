import requests
import os.path
from bs4 import BeautifulSoup

from watcher.watcher import Watcher

class PepperWatcher(Watcher):
    watcher_name = 'Pepper'
    filename = ''
    search_keyword = 'prijsfout'

    def generate_filename(self):
        self.filename = 'site_pepper_{0}.txt'.format(self.search_keyword)

    def parse_site(self):
        self.generate_filename()
        cookies = dict(sort_by="eyJpdiI6InhLQVwvVjdpV01Sblc5clZJV3FUT1FDdDIxdm1OUHRFM2V0SnBtSmhOK2ZBPSIsInZhbHVlIjoiU1RKV3EwSzM0Q0QwSitOUkwrVzVNZUpPeVBMbEhqWEVMcCtlbldiWm1FOD0iLCJtYWMiOiJlZTI3Yzc2MGU3YzEwZTg1NDRjMDVhMWU5ZGE0MDkwYzU3YTAxNWU0OWQyZWRlOTg5NmUxOTgzYzA4M2QxOGQ3In0=")
        result = requests.get("https://nl.pepper.com/search?q={0}".format(self.search_keyword), cookies=cookies)
        content = result.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup.find_all('a', class_='thread-title-text', limit=1)[0].get_text()

    def check_price_error(self):
        articles = self.parse_site()
        message_text = 'Zoekterm: {0} | *PRIJSFOUT GEVONDEN OP PEPPER*: {1}'.format(self.search_keyword, articles)

        if not os.path.isfile(self.filename):
            self.write_to_file(self.filename, articles)
            exit(0)
        else:
            with open(self.filename, 'r') as f:
                file_content = f.read().replace('\n', '')

                if file_content != articles:
                    self.send_telegram(self.watcher_name, message_text)
            self.write_to_file(self.filename, articles)
