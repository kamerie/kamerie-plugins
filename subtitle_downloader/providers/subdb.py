import hashlib
import os

import requests

from subtitle_downloader.subtitle_provider import SubtitleProvider


response = {
    "languages": {
        200: "Success",
        404: "Malformed"
    }
}

class SubDB(SubtitleProvider):
    def __init__(self, host, docs, cls, plugin_details, read_size, actions, useragent):
        super(SubDB, self).__init__(host, docs, cls, plugin_details)
        self.read_size = read_size
        self.actions = actions
        self.useragent = useragent.format(version=plugin_details.get('version', ''))

    def get_subtitles(self, subs):
        print 'subdb'

    def get_hash(self, path):
        with open(path, 'rb') as f:
            data = f.read(self.read_size)
            f.seek(-self.read_size, os.SEEK_END)
            data += f.read(self.read_size)
        return hashlib.md5(data).hexdigest()

    def _request(self, action, term, versions=False, language="en"):
        if action not in self.actions:
            raise NameError('action %s is not a viable action (%s) - package.json')

        # TODO: make async
        response = requests.get(self.host.format(query='{action}={term}'.format(action=action, term=term)))
        return response