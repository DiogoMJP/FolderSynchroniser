from datetime import datetime
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
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Open Directory', command=self.select_file)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.root.quit)

        self.main_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).place(relx=0.5, rely=0.5, anchor="center")

        self.opened_dirs = None

        self.root.mainloop()
    

    def select_file(self):
        selected_file = filedialog.Directory().show()
        
        if selected_file != "":
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        
        if self.opened_dirs == None:
            self.opened_dirs = Directory.Directory(None)
        self.opened_dirs.traverse_dirs(selected_file, selected_file)

        self.tree = ttk.Treeview(columns=["Last Modified", "Last Modification Origin"])
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.main_frame)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.main_frame)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.main_frame)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.tree.tag_configure('copy', background='light green')

        for col in ["Last Modified", "Last Modification Origin"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        
        self.opened_dirs.display(self.tree, '')


if __name__ == "__main__":
    app = App()