import os

from template import TemplatePlugin

TYPE_MOVIE = 'movie'
TYPE_SERIES = 'series'


class MediaScanner(TemplatePlugin):
    def scan_directory(self, dir, media_type):
        if media_type not in [TYPE_MOVIE, TYPE_SERIES]:
            self._logger.error('media_type wrong: %s' % media_type)

        for dirname, dirnames, filenames in os.walk('.'):
            for file in filenames:
                attributes = self.parse_file(dirname=dirname, file=file, media_type=media_type)
                self.add_file_to_library(file, **attributes)

    def parse_file(self, dirname, file, media_type):
        self._logger.info('parsing %s: %s' % media_type, os.path.join(dirname, file))
        return {}

    def add_file_to_library(self, file, **attributes):
        pass