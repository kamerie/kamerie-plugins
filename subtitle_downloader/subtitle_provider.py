class SubtitleProvider(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_subtitles(self, subs):
        raise NotImplementedError('n00b')