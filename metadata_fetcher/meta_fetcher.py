from kamerie.utilities.consts import MEDIA_TYPE, MEDIA_PATH, TYPE_SERIES, TYPE_MOVIE
from kamerie.utilities.utilities import get_logger
from media_item import MediaItem
from providers import PROVIDERS

class MetaFetcher(object):
    def __init__(self, **media_info):
        self.media_item = MediaItem(**media_info)
        self._logger = get_logger('meta_fetcher')

    def fetch_metadata(self):
        for provider in PROVIDERS[self.media_item.type]:
            self._logger.info('Using %s provider for %s' % (provider.__name__, self.media_item.name))
            provider().fetch_metadata(self.media_item)
            self._logger.info('Finished using %s provider for %s' % (provider.__name__, self.media_item.name))
