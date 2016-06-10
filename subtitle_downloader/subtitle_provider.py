class SubtitleProvider(object):
    def __init__(self, host, docs, cls, plugin_details, **kwargs):
        self.host = host
        self.docs = docs
        self.cls = cls

    def get_subtitles(self, subs):
        raise NotImplementedError('n00b')
