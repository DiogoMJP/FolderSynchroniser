from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

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

        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)

        self.main_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.main_frame.grid(row = 0, column = 0, padx=5, pady=5, sticky = "nesw")

        tk.Button(self.main_frame, text="Select Directory", anchor="center", justify="center", command=self.select_file).pack(expand=True, fill="both")

        self.opened_dirs = Directory.Directory()

        self.root.mainloop()
    

    # def traverse_dir(self, tv, parent,path):
    #     for d in os.listdir(path):
    #         full_path=os.path.join(path,d)
    #         isdir = os.path.isdir(full_path)
    #         id=tv.insert(parent,'end',text=d + "\t-\t" + str(datetime.fromtimestamp(os.path.getmtime(full_path))),open=False)
    #         if isdir:
    #             self.traverse_dir(tv, id,full_path)


    def select_file(self):
        selected_file = filedialog.Directory().show()
        
        if selected_file != "":
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        
        self.opened_dirs.traverse_dirs(selected_file)
            
        # selected_file = filedialog.Directory().show()
        
        # if selected_file != "":
        #     for widget in self.main_frame.winfo_children():
        #         widget.destroy()
        
        #     tv = ttk.Treeview(self.main_frame, show="tree")
        #     ybar=tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=tv.yview)
        #     tv.configure(yscroll=ybar.set)
        #     tv.heading('#0',text='Dir：'+selected_file,anchor='w')
        #     node=tv.insert('','end',text=selected_file,open=True)

        #     self.traverse_dir(tv, node, selected_file)

        #     ybar.pack(side=tk.RIGHT,fill=tk.Y)
        #     tv.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()