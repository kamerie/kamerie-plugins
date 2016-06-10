from subtitle_downloader.subtitle_provider import SubtitleProvider


class OpenSubtitles(SubtitleProvider):
    def __init__(self, host, docs, cls, plugin_details, **kwargs):
        super(OpenSubtitles, self).__init__(host, docs, cls, plugin_details, **kwargs)

    def get_subtitles(self, subs):
        print 'opensubtitles'