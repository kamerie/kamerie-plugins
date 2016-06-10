import os
import unittest

from subtitle_downloader.plugin import Plugin


class PluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('subtitle_downloader', path=os.path.split(os.getcwd())[0])

    def test_standard_initialization(self):
        message = None
        self.plugin.on_message(message)