from template_plugin.template import TemplatePlugin


class Plugin(TemplatePlugin):
    def on_message(self, message):
        print 'akabulbul', message


if __name__ == '__main__':
    Plugin('metadata_fetcher').start()
