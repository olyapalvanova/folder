import gzip
import os
import shutil


class Folder:
    def create(self, absolute_path):
        try:
            os.makedirs(absolute_path)
        except OSError as e:
            return e
        return 'Folder created'

    def clean(self, folder_name):
        try:
            shutil.rmtree(folder_name)
        except FileNotFoundError as e:
            return e
        return 'Folder cleaned'

    @classmethod
    def read(cls, folder_name):
        with open('folder structure.txt', 'w') as f:
            for _, dirs, _ in os.walk(folder_name):
                for dir in dirs:
                    f.write('/{}\n'.format(dir))
        return 'Sub folder structure created'

    @classmethod
    def compress(cls, folder_name):
        try:
            archived_folders = shutil.make_archive('archived_folders', 'zip',
                                                   folder_name)
        except FileNotFoundError as e:
            return e
        with open(archived_folders, 'rb') as f_in, gzip.open('folders_gzip.gz',
                                                             'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(archived_folders)
        return 'Folders was compressed'
