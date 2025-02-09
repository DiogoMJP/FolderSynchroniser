from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


left_file = None
right_file = None


def traverse_dir(tv, parent,path):
    for d in os.listdir(path):
        full_path=os.path.join(path,d)
        isdir = os.path.isdir(full_path)
        id=tv.insert(parent,'end',text=d + "\t-\t" + str(datetime.fromtimestamp(os.path.getmtime(full_path))),open=False)
        if isdir:
            traverse_dir(tv, id,full_path)


def select_left_file():
    global left_file
    left_file = filedialog.Directory().show()
    
    if left_file != "":
        for widget in left_frame.winfo_children():
            widget.destroy()
    
        tv = ttk.Treeview(left_frame, show="tree")
        ybar=tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscroll=ybar.set)
        tv.heading('#0',text='Dir：'+left_file,anchor='w')
        node=tv.insert('','end',text=left_file,open=True)

        traverse_dir(tv, node, left_file)

        ybar.pack(side=tk.RIGHT,fill=tk.Y)
        tv.pack(expand=True, fill="both")


def select_right_file():
    global right_file
    right_file = filedialog.Directory().show()
    
    if right_file != "":
        for widget in right_frame.winfo_children():
            widget.destroy()
    
        tv = ttk.Treeview(right_frame, show="tree")
        ybar=tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscroll=ybar.set)
        tv.heading('#0',text='Dir：'+right_file,anchor='w')
        node=tv.insert('','end',text=right_file,open=True)

        traverse_dir(tv, node, right_file)

        ybar.pack(side=tk.RIGHT,fill=tk.Y)
        tv.pack(expand=True, fill="both")


root = tk.Tk()
root.geometry("800x600+100+100")
root.title("File Synchronizer")

menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Select Left Directory', command=select_left_file)
filemenu.add_command(label='Select Right Directory', command=select_right_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.grid_rowconfigure(0, weight = 1)

left_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1)
left_frame.grid(row = 0, column = 0, padx=5, pady=5, sticky = "nesw")

right_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1)
right_frame.grid(row = 0, column = 1, padx=5, pady=5, sticky="nesw")

tk.Label(left_frame, text="No Directory Selected", anchor="center", justify="center", fg="gray", font=("Arial", 10, "bold"), ).pack(expand=True, fill="both")
tk.Label(right_frame, text="No Directory Selected", anchor="center", fg="gray", font=("Arial", 10, "bold"), ).pack(expand=True, fill="both")


root.mainloop()