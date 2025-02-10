import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.font as tkFont

import Directory



class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600+100+100")
        self.root.title("File Synchronizer")

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label='Open Directory', command=self.select_file)
        menu.add_command(label='Refresh Files', command=self.refresh_files)
        menu.add_command(label='Clear Selection', command=self.clear_selection)
        menu.add_command(label='Synchronise Files', command=self.sync_files)

        self.main_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).place(relx=0.5, rely=0.5, anchor="center")

        self.opened_dirs = None
        self.path_origins = []

        self.root.mainloop()
    

    def select_file(self):
        selected_file = filedialog.Directory().show()
        
        if selected_file != "":
            if self.opened_dirs == None:
                self.opened_dirs = Directory.Directory(None)
                
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            self.path_origins += [selected_file]
            
            self.opened_dirs.traverse_dirs(selected_file, selected_file)
            self.opened_dirs.check_for_number_of_files(len(self.path_origins))

            self.tree = ttk.Treeview(self.main_frame, columns=["Last Modified", "Last Modification Origin"])
            self.tree.pack(expand=True, fill="both", padx=5, pady=5)
            self.tree.tag_configure('copy', background='light green')

            for col in ["Last Modified", "Last Modification Origin"]:
                self.tree.heading(col, text=col.title())
                self.tree.column(col, width=tkFont.Font().measure(col.title()))
            
            self.opened_dirs.display(self.tree, '')
    

    def refresh_files(self):
        if self.opened_dirs == None:
            return
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.tree = ttk.Treeview(self.main_frame, columns=["Last Modified", "Last Modification Origin"])
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)
        self.tree.tag_configure('copy', background='light green')

        for col in ["Last Modified", "Last Modification Origin"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        
        self.opened_dirs = Directory.Directory(None)
        for path in self.path_origins:
            self.opened_dirs.traverse_dirs(path, path)
        self.opened_dirs.check_for_number_of_files(len(self.path_origins))

        self.opened_dirs.display(self.tree, '')
    

    def clear_selection(self):
        self.opened_dirs = None
        self.origin_paths = []

        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).place(relx=0.5, rely=0.5, anchor="center")
    

    def sync_files(self):
        if self.opened_dirs != None:
            self.opened_dirs.update_files({path : os.path.normpath(path) for path in self.path_origins})
        else:
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.tree = ttk.Treeview(self.main_frame, columns=["Last Modified", "Last Modification Origin"])
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)
        self.tree.tag_configure('copy', background='light green')

        for col in ["Last Modified", "Last Modification Origin"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        
        self.opened_dirs = Directory.Directory(None)
        for path in self.path_origins:
            self.opened_dirs.traverse_dirs(path, path)
        self.opened_dirs.check_for_number_of_files(len(self.path_origins))

        self.opened_dirs.display(self.tree, '')
        



if __name__ == "__main__":
    app = App()