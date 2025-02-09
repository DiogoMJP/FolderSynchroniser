import os


class File():
    def __init__(self):
        self.origin = None
        self.dest_list = []

    def update_path(self, path):
        if self.origin == None:
            self.origin = {"path" : path, "time" : os.path.getmtime(path)}
        print(self.origin)