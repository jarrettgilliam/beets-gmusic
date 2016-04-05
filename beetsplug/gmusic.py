import logging
from beets.plugins import BeetsPlugin
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

        # Initialize gmusicapi
        self.mm = Musicmanager(debug_logging=False)
        self.mm.logger.addHandler(logging.NullHandler())
        try:
            if not self.mm.login(oauth_credentials=OAUTH_FILEPATH, uploader_id=self.uploader_id):
                try:
                    self.mm.perform_oauth()
                except e:
                    self._log.error("Error: Unable to login with specified oauth code.")
                    raise e
                self.mm.login(oauth_credentials=OAUTH_FILEPATH, uploader_id=self.uploader_id)
        except (OSError, ValueError) as e:
            self._log.error("Error: Couldn't log in.")
            raise e

        if not self.mm.is_authenticated():
            self._log.error("Error: Couldn't log in.")
            raise RuntimeError("Error: Couldn't log in.")

        # Register listeners
        if self.auto_upload:
            self.register_listener('item_imported', self.on_item_imported)
            self.register_listener('album_imported', self.on_album_imported)

    def on_item_imported(self, lib, item):
        uploaded, matched, not_uploaded = \
                self.mm.upload(item.path, enable_matching=self.enable_matching)
        if uploaded:
            self._log.info('Successfully uploaded "{0}"'.format(item.path))
        elif matched:
            self._log.info('Successfully scanned and matched "{0}"'.format(item.path))
        else:
            self._log.warning('Warning: {0}'.format(not_uploaded[item.path]))

    def on_album_imported(self, lib, album):
        for item in album.items():
            self.on_item_imported(lib, item)

