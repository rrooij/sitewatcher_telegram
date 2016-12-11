import requests
import config

class Watcher:

    def write_to_file(self, filename, content):
        with open(filename, 'w') as file:
            file.write(content)


    def send_telegram(self, message):
        chat_ids = config.chat_ids
        for chat_id in chat_ids:
            requests.get("https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(config.bot_password, chat_id, message))

    def parse_site(self):
        raise NotImplementedError("Implement this method")

    def check_price_error(self):
        raise NotImplementedError("Implement this method")
