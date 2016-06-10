import os
import unittest

from subtitle_downloader.plugin import Plugin


class PluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('subtitle_downloader', path=os.path.split(os.getcwd())[0])

    def test_standard_initialization(self):
        message = None
        try:
            self.plugin.on_message(message)
        except Exception as e:
            self.fail("Error initializing %s" % e)

    def test_unregistered_providers_arent_added(self):
        providers = {
            "test_provider": {}
        }

        verified_providers = self.plugin.register_providers(providers)
        self.assertFalse(verified_providers, "invalid provider was registered")