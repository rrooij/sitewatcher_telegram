from watcher.pepperwatcher import PepperWatcher
from watcher.tweakerswatcher import TweakersWatcher

pepper = PepperWatcher()
pepper.check_price_error()
tweakers = TweakersWatcher()
tweakers.check_price_error()