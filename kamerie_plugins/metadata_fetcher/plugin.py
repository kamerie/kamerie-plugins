from kamerie.template.template import TemplatePlugin
from kamerie_plugins.metadata_fetcher.meta_fetcher import MetaFetcher


class Plugin(TemplatePlugin):
    def on_message(self, message):
        print "Metadata Fetcher received", str(message)
        MetaFetcher(message['type']).fetch_metadata(message)


if __name__ == '__main__':
    Plugin('metadata_fetcher').start()
