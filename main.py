import gzip
import os
import shutil


class Folder:
    class FolderException(Exception):
        pass

    ARCHIVED_FOLDERS = 'archived_folders'
    GZIP_FOLDERS = 'folders_gzip.gz'

    def __init__(self, path, parent=None):
        self.path = path
        self.children = list()
        self.parent = parent
        if parent:
            parent.add_child(self)

    @property
    def full_path(self) -> str:
        if self.parent:
            return os.path.join(self.parent.full_path, self.path)
        return self.path

    def is_exists_in_children(self, folder):
        is_exists_folder = [child.path == folder.path for child in self.children]
        return True in is_exists_folder

    def add_child(self, folder: 'Folder'):
        if self.is_exists_in_children(folder):
            raise self.FolderException(
                'Folder is already assigned to parent folder'
            )
        folder.parent = self
        self.children.append(folder)

    def remove_child(self, folder: 'Folder'):
        if not self.is_exists_in_children(folder):
            raise self.FolderException(
                'Folder is not assigned to parent folder'
            )
        self.children.remove(folder)

    def print_tree(self, indent=0):
        indent_str = indent * ' '
        print(f'{indent_str} {self.path}')
        for child in self.children:
            child.print_tree(indent=indent + 4)

    def create(self):
        try:
            os.makedirs(self.full_path)
        except FileExistsError as e:
            raise self.FolderException() from e
        for child in self.children:
            child.create()

    def clean(self):
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError as e:
            raise self.FolderException() from e

    @staticmethod
    def read(path):
        list_dirs = []
        for _, dirs, _ in os.walk(path):
            for folder in dirs:
                list_dirs.append('/{}'.format(folder))
        return list_dirs

    def compress(self):
        try:
            archived_folders = shutil.make_archive(
                self.ARCHIVED_FOLDERS, 'zip', self.path
            )
        except FileNotFoundError as e:
            raise e
        with open(archived_folders, 'rb') as f_in, gzip.open(
                self.GZIP_FOLDERS, 'wb'
        ) as f_out:
            f_out.writelines(f_in)
        os.remove(archived_folders)
