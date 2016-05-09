from kamerie.template import TemplatePlugin
from meta_fetcher import MetaFetcher


class Plugin(TemplatePlugin):
    def on_message(self, message, received="Metadata Fetcher received"):
        print received, str(message)
        MetaFetcher(message['type']).fetch_metadata(message)


if __name__ == '__main__':
    Plugin('metadata_fetcher').start()
