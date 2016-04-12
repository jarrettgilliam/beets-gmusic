import logging
import time
from threading import Thread
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs
from gmusicapi.clients import Musicmanager, OAUTH_FILEPATH

class GooglePlayMusicPlugin(BeetsPlugin):
    def __init__(self):
        super(GooglePlayMusicPlugin, self).__init__()

        # Get configurations
        self.config.add({
            'auto-upload': True,
            #'auto-delete': True,
            'enable-matching': True,
            'uploader-id': None
        })
        self.auto_upload = self.config['auto-upload'].get(bool)
        #self.auto_delete = self.config['auto-delete'].get(bool)
        self.enable_matching = self.config['enable-matching'].get(bool)
        self.uploader_id = self.config['uploader-id'].get()
        self.concurrent_uploads = 5

        # Initialize gmusicapi
        self.mm = Musicmanager(debug_logging=False)
        self.mm.logger.addHandler(logging.NullHandler())
        if not self.__mm_authenticate():
            self._log.warning('Warning: oauth failed.')

        # Register listeners
        if self.auto_upload:
            self.register_listener('item_imported', self.on_item_imported)
            self.register_listener('album_imported', self.on_album_imported)

    def on_item_imported(self, lib, item):
        self.__upload_item(item)

    def on_album_imported(self, lib, album):
        self.__upload_items(album.items())

    def commands(self):
        gmupload_cmd = Subcommand('gmupload', help='upload songs to Google Play Music matching a query')

        def on_gmupload(lib, opts, args):
            self.__upload_items(lib.items(decargs(args)))

        gmupload_cmd.func = on_gmupload

        return [gmupload_cmd]

    def __mm_authenticate(self):
        if not self.mm.is_authenticated():
            try:
                if not self.mm.login(oauth_credentials=OAUTH_FILEPATH, uploader_id=self.uploader_id):
                    try:
                        self.mm.perform_oauth()
                    except e:
                        self._log.error("Error: Unable to login with specified oauth code.")
                        return False
                    if not self.mm.login(oauth_credentials=OAUTH_FILEPATH, uploader_id=self.uploader_id):
                        return False
            except (OSError, ValueError) as e:
                self._log.error("Error: Couldn't log in.")
                return False
        return True


    def __upload_item(self, item):
        if not self.__mm_authenticate():
            self._log.warning('Warning: Not logged in. Can\'t upload "{0}'.format(item.path))
        else:
            uploaded, matched, not_uploaded = \
                self.mm.upload(item.path, enable_matching=self.enable_matching)
            if uploaded:
                self._log.info('Successfully uploaded "{0}"'.format(item.path))
            elif matched:
                self._log.info('Successfully scanned and matched "{0}"'.format(item.path))
            else:
                self._log.warning('Warning: {0}'.format(not_uploaded[item.path]))

    def __upload_items(self, items):
        # Upload n items at a time
        threads = []
        i = 0
        while (i < len(items)):
            if (len(threads) < self.concurrent_uploads):
                t = Thread(target=self.__upload_item, args=(items[i],))
                t.start()
                threads.append(t)
                i += 1
            else:
                j = 0
                while (j < len(threads)):
                    if not threads[j].is_alive():
                        threads.pop(j)
                        break
                    j += 1
                else:
                    time.sleep(3)
        for t in threads:
            t.join()

