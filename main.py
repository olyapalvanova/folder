import gzip
import os
import shutil


class Folder:
    MESSAGE = 'Path was wrong. Check it and try again.'

    def __init__(self, path, parent=None):
        if isinstance(parent, Folder):
            self.path = parent.path + path
        else:
            self.path = path

    def create(self):
        try:
            os.makedirs(self.path)
        except OSError:
            return self.MESSAGE

    def clean(self):
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            return self.MESSAGE

    @classmethod
    def read(cls, path):
        with open('folder structure.txt', 'w') as f:
            for _, dirs, _ in os.walk(path):
                for dir in dirs:
                    f.write('/{}\n'.format(dir))

    def compress(self):
        try:
            archived_folders = shutil.make_archive('archived_folders', 'zip',
                                                   self.path)
        except FileNotFoundError:
            return self.MESSAGE
        with open(archived_folders, 'rb') as f_in, gzip.open('folders_gzip.gz',
                                                             'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(archived_folders)
