
import scan

class MediaData:
    def __init__(self):
        pass

    def scan_for_files(self, media_dir):
        self._media_dir = media_dir

        self._files = scan.Files()
        self._files.scan_tree(media_dir, scan.MOVIE_EXTS)

    def _get_media_files(self):
        return self._files.file_list

    file_paths = property(_get_media_files)
