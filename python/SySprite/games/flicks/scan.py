
import os
import hashlib


MOVIE_EXTS = ('.mov', '.avi', '.mpg')


class Files:
    def __init__(self):
        pass

    def scan_tree(self, root, exts):
        """ Look in a directory for filenames with given extensions. """

        files = []
        for (dirpath, dirnames, filenames) in os.walk(root):
            for f in filenames:
                fn,ext = os.path.splitext(f)
                if ext.lower() in exts:
                    fname = os.path.join(dirpath,f)
                    files.append(fname)

        #print files

        # now create hashes to identify files uniquely, as they could move
        self.hashes = {}
        for f in files:
            m = hashlib.md5()
            with open(f, 'rb') as fh:
                m.update(fh.read(1024*1024))
                self.hashes[m.digest()] = f

        #print self.hashes

    file_list = property(lambda self: self.hashes.values())


if __name__=='__main__':
    f = Files()
    f.scan('.', MOVIE_EXTS)
    f.calc_hashes()
