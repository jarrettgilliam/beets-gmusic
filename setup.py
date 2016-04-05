from setuptools import setup, find_packages

setup(
    name = "beets-gmusic",
    version = "0.0.1-dev",
    description="beets plugin to sync music library with Google Play Music",
    long_description=open('README.md').read(),
    author='Jarrett Gilliam',
    author_email='jarrettgilliam@gmail.com',
    url='https://github.com/jarrettgilliam/beets-gmusic',
    download_url='https://github.com/jarrettgilliam/beets-gmusic.git',
    license='MIT',

    packages=['beetsplug'],
    namespace_packages=['beetsplug'],
    install_requires = ['beets>=1.3.17','gmusicapi>=9.0.0']
)
