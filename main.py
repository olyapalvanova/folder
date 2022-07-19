import gzip
import os
import shutil


class Folder:
    def __init__(self, path):
        self.path = path

    def create(self):
        try:
            os.makedirs(self.path)
        except OSError:
            return 'Path was wrong. Check it and try again.'

    def clean(self):
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            return 'Path was wrong. Check it and try again.'

    @classmethod
    def read(cls, path):
        with open('folder structure.txt', 'w') as f:
            for _, dirs, _ in os.walk(path):
                for dir in dirs:
                    f.write('/{}\n'.format(dir))
        return cls(path)

    def compress(self):
        try:
            archived_folders = shutil.make_archive('archived_folders', 'zip',
                                                   self.path)
        except FileNotFoundError:
            return 'Path was wrong. Check it and try again.'
        with open(archived_folders, 'rb') as f_in, gzip.open('folders_gzip.gz',
                                                             'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(archived_folders)
