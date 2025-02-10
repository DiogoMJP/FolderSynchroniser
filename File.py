from datetime import datetime
import os
import tkinter.font as tkFont


class File():
    def __init__(self, file_name):
        self.file_name = file_name
        self.origin = None
        self.dest_list = []
        self.copy = False

    def update_path(self, path, path_origin):
        time = os.path.getmtime(path)
        if self.origin == None:
            self.origin = (path, time, path_origin)
        else:
            if time > self.origin[1]:
                origin = self.origin
                self.dest_list += [origin]
                self.origin = (path, time, path_origin)
                self.copy = True
            else:
                self.dest_list += [(path, time, path_origin)]
                if time < self.origin[1]:
                    self.copy = True


    def display(self, tree, parent):
        item = (datetime.fromtimestamp(self.origin[1]), self.origin[2])
        if self.copy:
            tree.insert(parent, 'end', text=self.file_name, values=item, tags=("copy",))
        else:
            tree.insert(parent, 'end', text=self.file_name, values=item)