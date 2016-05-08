from setuptools import setup, find_packages

from kamerie_plugins import list_plugins, get_plugin_requirements

MANDATORY_LIBRARIES = ['pika', 'pymongo']


def get_requirements_for_plugins():
    return map(lambda f: get_plugin_requirements(f), list_plugins())


setup(
    name='kamerie_plugins',
    version='0.1',
    author='Chen Asraf & Dor Munis',
    url='https://github.com/kamerie/kamerie_plugins',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'kamerie_plugins': ['*']},
    platforms='any',
    license='Apache 2.0',
    install_requires=[] + MANDATORY_LIBRARIES + get_requirements_for_plugins(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)