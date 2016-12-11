import requests
import config

class Watcher:

    def write_to_file(self, filename, content):
        with open(filename, 'w') as file:
            file.write(content)


    def send_telegram(self, watcher_name, message):
        chat_ids = config.chat_ids
        for chat_id in chat_ids:
            payload = { 'chat_id': chat_id, 'text': '[{0}]: {1}'.format(watcher_name, message) }
            requests.get("https://api.telegram.org/bot{0}/sendMessage".format(config.bot_password), params=payload)

    def parse_site(self):
        raise NotImplementedError("Implement this method")

    def check_price_error(self):
        raise NotImplementedError("Implement this method")
