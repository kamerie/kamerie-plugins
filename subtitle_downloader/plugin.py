import imp
import os
from copy import deepcopy

from kamerie.template import TemplatePlugin
from subtitle_downloader.subtitle_provider import SubtitleProvider


class Plugin(TemplatePlugin):
    def __init__(self, plugin_name, path):
        super(Plugin, self).__init__(plugin_name, path)

        # provider handling
        provider_list = self.__dict__.get('settings', [])
        self.providers = self.register_providers(provider_list)

    def on_message(self, message):
        for provider in self.providers:
            subtitles = provider.get_subtitles(message)
            self.handle_result(subtitles)

    def register_providers(self, providers):
        valid_subtitles_providers = []

        for module, provider in providers.iteritems():
            module = '{module}.py'.format(module=module)
            expected_class = provider.get('cls', '')

            try:
                subtitle_module = imp.load_source('providers.%s' % module, os.path.join(self.path, 'providers', module))
                if hasattr(subtitle_module, expected_class):
                    settings = deepcopy(provider)
                    settings.pop('cls')
                    subtitle_provider = getattr(subtitle_module, expected_class)(path=self.path, **settings)
                    if isinstance(subtitle_provider, SubtitleProvider):
                        valid_subtitles_providers.append(subtitle_provider)
                    else:
                        self._logger.error('%s is not a viable subtitle provider class' % expected_class)
                else:
                    self._logger.error('module {module} does not have a class called: {cls}'.
                                       format(module=module, cls=expected_class))
            except IOError:
                self._logger.error('no module found: %s' % module)

        return valid_subtitles_providers

    def handle_result(self, subs):
        pass