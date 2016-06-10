from subtitle_downloader.subtitle_provider import SubtitleProvider


class OpenSubtitles(SubtitleProvider):
    def get_subtitles(self, subs):
        print 'opensubtitles'