import os

import File



class Directory:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.subdirs = {}
        self.files = {}


    def traverse_dirs(self, path, path_origin):
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
    

    def display(self, tree, parent):
        if self.dir_name != None:
            id = tree.insert(parent, 'end', text=self.dir_name)
        else:
            id = ''

        for file in self.files.values():
            file.display(tree, id)
        for dir in self.subdirs.values():
            dir.display(tree, id)