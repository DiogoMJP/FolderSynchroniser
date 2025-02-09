import os

import File


class Directory:
    def __init__(self):
        self.subdirs = {}
        self.files = {}
    
    def traverse_dirs(self, path):
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            isdir = os.path.isdir(full_path)

            if isdir:
                if d in self.subdirs.keys():
                    self.subdirs[d].traverse_dirs(full_path)
                else:
                    self.subdirs[d] = Directory()
                    self.subdirs[d].traverse_dirs(full_path)

            else:
                if d in self.files.keys():
                    self.files[d].update_path(full_path)
                else:
                    self.files[d] = File.File()
                    self.files[d].update_path(full_path)