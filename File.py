import os


class File():
    def __init__(self):
        self.origin = None
        self.dest_list = []

    def update_path(self, path):
        time = os.path.getmtime(path)
        if self.origin == None:
            self.origin = {"path" : path, "time" : time}
        else:
            if time > self.origin["time"]:
                origin = self.origin
                self.dest_list += [origin]
                self.origin = {"path" : path, "time" : time}
            else:
                self.dest_list += [{"path" : path, "time" : time}]
        print(self.origin)