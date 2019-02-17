from watcher.bolwatcher import BolWatcher
from watcher.pepperwatcher import PepperWatcher
from watcher.tweakerswatcher import TweakersWatcher

pepper = PepperWatcher()
pepper.check_price_error()
pepper.search_keyword = 'fout'
pepper.check_price_error()
tweakers = TweakersWatcher()
tweakers.check_price_error()
bol = BolWatcher()
bol.check_price_error()
