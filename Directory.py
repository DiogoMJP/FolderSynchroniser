import os
from tkinter import ttk

import File



class Directory(object):
    """ Represents each directory that is found recursively and stores its subdirectories\n
        and subfiles """

    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        self.subdirs = {}
        self.files = {}


    def traverse_dirs(self, path: str, path_origin: str) -> None:
        """ Goes recursively through each subdirectory of the opened directory;\n
            opening or creating the corresponding objects """
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            isdir = os.path.isdir(full_path)

            if isdir:
                if d in self.subdirs.keys():
                    self.subdirs[d].traverse_dirs(full_path, path_origin)
                else:
                    self.subdirs[d] = Directory(d)
                    self.subdirs[d].traverse_dirs(full_path, path_origin)

            else:
                if d in self.files.keys():
                    self.files[d].update_path(full_path, path_origin)
                else:
                    self.files[d] = File.File(d)
                    self.files[d].update_path(full_path, path_origin)
    

    def check_for_number_of_files(self, number: int) -> None:
        """  """
        for dir in self.subdirs.values():
            dir.check_for_number_of_files(number)
        for file in self.files.values():
            file.check_for_number_of_files(number)
    

    def display(self, tree: ttk.Treeview, parent: str) -> None:
        """ Displays this directory, showing its name, and recursively\n
            displays each subdirectory and subfile """
        if self.dir_name != None:
            id = tree.insert(parent, 'end', text=self.dir_name)
        else:
            id = ''

        for file in self.files.values():
            file.display(tree, id)
        for dir in self.subdirs.values():
            dir.display(tree, id)


    def update_files(self, path_origins: list[tuple[str, str]]) -> None:
        """ Recursively synchronises each subdirectory and subfile\n
            inside this directory """
        if self.dir_name != None:
            path_origins = {path[0] : os.path.normpath(os.path.join(path[1], self.dir_name)) for path in path_origins.items()}
        for file in self.files.values():
            file.update_files(path_origins)
        for dir in self.subdirs.values():
            dir.update_files(path_origins)