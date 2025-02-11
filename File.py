from datetime import datetime
import os
import shutil
from tkinter import ttk


class File(object):
    """ For each file contained in the given directories, this object stores the different\n
        directories where this file is saved along with their last modification time """

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.origin = None
        self.dest_list = {}
        self.copy = False

    def update_path(self, path: str, path_origin: str) -> None:
        """ Receives a new path where this file is stored and updates the file\n
            that serves as origin for the copy depending on what file is the most\n
            recent """
        time = os.path.getmtime(path)
        if self.origin == None:
            self.origin = {"path" : path_origin, "time" : time}
        else:
            if time > self.origin["time"]:
                temp = self.origin
                self.dest_list[temp["path"]] = temp["time"]
                self.origin = {"path" : path_origin, "time" : time}
                self.copy = True
            else:
                self.dest_list[path_origin] = time
                if time < self.origin["time"]:
                    self.copy = True
    

    def check_for_number_of_files(self, number: int) -> None:
        """ Checks if the number of files that was found is the same as the number\n
            of directories that have been opened\n
            If not, then the file is marked as needing to be copied """
        if len(self.dest_list.items()) + 1 < number:
            self.copy = True 


    def display(self, tree: ttk.Treeview, parent: str) -> None:
        """ Displays this file; showing the file name, the last time it was modified,\n
            and the origin of the file that was last modified\n
            It is displayed in green if the file needs to be copied """
        item = (datetime.fromtimestamp(self.origin["time"]), self.origin["path"])
        if self.copy:
            tree.insert(parent, 'end', text=self.file_name, values=item, tags=("copy",))
        else:
            tree.insert(parent, 'end', text=self.file_name, values=item)
    

    def update_files(self, path_origins: list[tuple[str, str]]) -> None:
        """ Copies the most recent version of the file to the corresponding\n
            folder in each opened directory """
        path_origins = {path[0] : os.path.normpath(os.path.join(path[1], self.file_name)) for path in path_origins.items()}
        origin = path_origins[self.origin["path"]]
        for dest in [path for path in path_origins.keys() if path != self.origin["path"]]:
            if dest not in self.dest_list.keys() or self.dest_list[dest] < self.origin["time"]:
                dest_path = path_origins[dest]
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(origin, dest_path)