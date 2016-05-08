def list_plugins():
    from pkg_resources import resource_listdir as listdir
    from pkg_resources import resource_isdir as isdir
    return filter(lambda p: isdir(__name__, p) and p[0] != '.', listdir(__name__, ''))


def get_plugin_requirements(plugin):
    from os.path import join, exists

    requirements_file = join(plugin_path(plugin), 'requirements.txt')
    libraries = []

    if exists(requirements_file):
        with open(requirements_file, 'r') as f:
            libraries += f.readlines()

    return list(set(libraries))


def plugin_path(plugin):
    from pkg_resources import resource_filename as _get_plugin
    return _get_plugin(__name__, plugin)


def plugin_module(plugin):
    from os.path import join
    return join(plugin_path(plugin), 'plugin.py')


def register_plugins():
    from os.path import exists
    from imp import load_source

    plugin_list = []

    for plugin in list_plugins():
        config_path = plugin_module(plugin)
        config_import = load_source('kamerie_plugin_%s' % plugin, config_path)

        if exists(config_path):
            plugin_conf = {
                'name': plugin,
                'path': plugin_path(plugin),
                'config_path': config_path,
                'plugin_cls': config_import.Plugin(plugin)
            }
            plugin_list.append(plugin_conf)

    return plugin_list
