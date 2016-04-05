beets-gmusic
============

*Note: This project is very much still alpha quality. Some things may not work right and updates may break things. Use at your own risk.*

## Overview

This is a [Google Play Music][1] plugin for [beets][2]. It attempts to keep the two libraries in sync by:
 * Automatically uploading tracks during beets imports

#### TODO:
 * ~~Automatically deleting tracks with beets~~
 * ~~Automatically updating metadata with beets~~
 * ~~Syncing both libraries via the `gmsync` subcommand~~

## Installation

Make sure [beets][3] and [gmusicapi][4] are installed:
```
sudo pip install beets gmusicapi
```

Clone this repository and install:
```
git clone https://github.com/jarrettgilliam/beets-gmusic.git
cd beets-gmusic
sudo python setup.py install
```

*Note: To install for just the current user, replace the last line above with this one:*
```
python setup.py install --user
```

Add `gmusic` to the list of plugins in your [configuration file][5].

## Configuration

To configure, make a `gmusic:` section in your [configuration file][5]. The available options are:

 * **auto-upload**: Enable uploading of songs during imports. Default: `yes`.
 * **enable-matching**: Attempt to use scan and match to avoid uploading every song. This requires `ffmpeg` or `avconv`. Default `yes`.
 * **uploader-id**: A unique id such as a MAC address (ex: `'00:11:22:33:AA:BB'`). This should only be provided in cases where the default (host MAC address incremented by 1) will not work. Default `None`.

[1]: https://play.google.com/music/listen
[2]: http://beets.io/
[3]: http://beets.readthedocs.org/en/latest/guides/main.html
[4]: https://unofficial-google-music-api.readthedocs.org/en/latest/usage.html
[5]: http://beets.readthedocs.org/en/latest/reference/config.html
