import unittest

from subtitle_downloader.providers.subdb import SubDB

SANDBOX_URL = "http://sandbox.thesubdb.com/?action={query}"


class TestSubDB(unittest.TestCase):

    def setUp(self):
        self.subdb = SubDB(SANDBOX_URL, '', "SubDB", {'version': '1337'}, 65536, ["search", "download", "languages", "upload"], "SubDB/1.0 (Kamerie/{version}; https://github.com/kamerie)")

    def test_useragent(self):
        self.assertTrue("SubDB/1.0 (Kamerie/1337; https://github.com/kamerie)")