import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.font as tkFont

import Directory



class App(object):
    """ The main application for this program """

    def __init__(self):
        # Creates the window and sets its name
        self.root = tk.Tk()
        self.root.geometry("800x600+100+100")
        self.root.title("File Synchronizer")

        # Creates the menu bar on top
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label='Open Directory', command=self.select_file)
        menu.add_command(label='Refresh Files', command=self.refresh_files)
        menu.add_command(label='Clear Selection', command=self.clear_selection)
        menu.add_command(label='Synchronise Files', command=self.sync_files)

        # Creates a frame to store the main window information
        self.main_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1, background='white')
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Creates a secondary button to open a directory
        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).place(relx=0.5, rely=0.5, anchor="center")

        self.opened_dirs = None
        # Stores all starting paths for the opened directories
        self.path_origins = []

        self.root.mainloop()


    def create_tree(self) -> None:
        """ Creates the Treeview to display the directories """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.main_frame, columns=["Last Modified", "Last Modification Origin"])
        self.tree.pack(expand=True, fill="both")
        # Directories that will be copied are coloured light green
        self.tree.tag_configure('copy', background='light green')

        for col in ["Last Modified", "Last Modification Origin"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
    

    def select_file(self) -> None:
        """ Allows the user to select a directory to open\n
            Directories can't be opened within other opened directories """
        selected_file = filedialog.Directory().show()
        
        if selected_file != "":
            if self.opened_dirs == None:
                self.opened_dirs = Directory.Directory(None)
            
            self.path_origins += [selected_file]
            
            self.opened_dirs.traverse_dirs(selected_file, selected_file)
            self.opened_dirs.check_for_number_of_files(len(self.path_origins))

            self.create_tree()
            
            self.opened_dirs.display(self.tree, '')
    

    def refresh_files(self) -> None:
        """ Searches through all directories again to update if changes have been made """
        if self.opened_dirs == None:
            return
        
        self.create_tree()
        
        self.opened_dirs = Directory.Directory(None)
        for path in self.path_origins:
            self.opened_dirs.traverse_dirs(path, path)
        self.opened_dirs.check_for_number_of_files(len(self.path_origins))

        self.opened_dirs.display(self.tree, '')
    

    def clear_selection(self) -> None:
        """ Clears all directories from selection\n
            Clears the screen and restores the button to select directories """
        self.opened_dirs = None
        self.origin_paths = []

        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).place(relx=0.5, rely=0.5, anchor="center")
    

    def sync_files(self) -> None:
        """ Synchronises the contents of all the different directories to their most recent version """
        if self.opened_dirs == None:
            return
        
        self.opened_dirs.update_files({path : os.path.normpath(path) for path in self.path_origins})
        
        self.create_tree()
        
        self.opened_dirs = Directory.Directory(None)
        for path in self.path_origins:
            self.opened_dirs.traverse_dirs(path, path)
        self.opened_dirs.check_for_number_of_files(len(self.path_origins))

        self.opened_dirs.display(self.tree, '')
        



if __name__ == "__main__":
    app = App()