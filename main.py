import gzip
import os
import shutil


class Folder:
    ARCHIVED_FOLDERS = 'archived_folders'
    GZIP_FOLDERS = 'folders_gzip.gz'

    children = list()
    root_folder_id = list()

    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        if isinstance(parent, Folder):
            self.add_child()

    def add_child(self):
        if not self.children:
            self.root_folder_id.append(id(self.parent))
        if self.root_folder_id[0] != id(self.parent):
            if self.parent.path in self.children:
                self.children.remove(self.parent.path)
        self.path = os.path.join(self.parent.path, self.path)
        self.children.append(self.path)

    def print_tree(self):
        space = ' '
        space_count = 4
        tree = list()
        tree.append(self.path)
        for child in self.children:
            child = child.replace(self.path, '').replace('/', '', 1)
            child_folders = child.split('/')
            for i, folder in enumerate(child_folders):
                folder_name = (i + 1) * space_count * space + folder
                tree.append(folder_name)
        print('\n'.join(tree))

    def create(self):
        for child in self.children:
            if not os.path.exists(child):
                try:
                    os.makedirs(child)
                except OSError as e:
                    raise e
            else:
                continue
        self.children.clear()
        self.root_folder_id.clear()

    def clean(self):
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError as e:
            raise e

    @staticmethod
    def read(path):
        list_dirs = []
        for _, dirs, _ in os.walk(path):
            for folder in dirs:
                list_dirs.append('/{}\n'.format(folder))
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
