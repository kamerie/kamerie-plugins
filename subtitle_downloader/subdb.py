from subtitle_downloader.subtitle_provider import SubtitleProvider


class SubDB(SubtitleProvider):
    def get_subtitles(self, subs):
        print 'subdb'