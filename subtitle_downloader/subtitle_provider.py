class SubtitleProvider(object):
    def __init__(self, **settings):
        mandatory = ['host', 'docs', 'class']
        for item in mandatory:
            if item not in settings:
                raise NameError('%s is missing from the providers settings (package.json)')

        self.__dict__.update(settings)

    def get_subtitles(self, subs):
        raise NotImplementedError('n00b')
