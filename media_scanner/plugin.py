from media_scanner.media_scanner import MediaScanner, TYPE_MOVIE
from template_plugin.template import TemplatePlugin


class Plugin(TemplatePlugin):
    def on_message(self, message):
        print "Media Scanner plugin received message: %s from the other side" % message
        scanner = MediaScanner()
        scanner.scan_directory(message, TYPE_MOVIE)