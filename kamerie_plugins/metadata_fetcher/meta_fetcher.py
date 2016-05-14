from kamerie.utilities.consts import MEDIA_TYPE, MEDIA_PATH, TYPE_SERIES, TYPE_MOVIE
from media_item import MediaItem
from providers import PROVIDERS

class MetaFetcher(object):
    def __init__(self, **media_info):
        self.media_item = MediaItem(**media_info)

    def fetch_metadata(self):
        for provider in PROVIDERS[self.media_item.type]:
            provider().fetch_metadata(self.media_item)
