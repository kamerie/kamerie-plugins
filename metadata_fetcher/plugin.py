from kamerie.template import TemplatePlugin
from meta_fetcher import MetaFetcher
from kamerie.utilities.consts import MEDIA_TYPE
from pprint import pformat


class Plugin(TemplatePlugin):
    def on_message(self, message, received="Metadata Fetcher received: %s"):
        print received % pformat(message)
        
        try:
            MetaFetcher(**message).fetch_metadata()
        except AttributeError as e:
            self._logger.error(e)


if __name__ == '__main__':
    Plugin('metadata_fetcher').start()
