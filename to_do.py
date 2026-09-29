from tkinter import Tk, ttk
import tkinter as tk


notes = []
notes_count = 0

root = Tk(screenName="Py-To-Do", className ="To-Do".lower())

col0= 30
col2= 40
row0= 10
row1= 20

#menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

filemenu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Note",command=lambda: add_note())
filemenu.add_command(label="Open",command=lambda: open_note())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

#notes
lbl0 = tk.Label(root, width=col0, text=f"Notes: {len(notes)}")

scroll = tk.Scrollbar(root)
lb = tk.Listbox(root, width=col0, height=row0, yscrollcommand=scroll.set)
scroll.config(command=lb.yview)

btn = tk.Button(root, text="Add\t+", width=col0, command=lambda: add_note())
    
#entery
lbl_status = tk.Label(root, width=col2, text="Status: Todo")
entry = tk.Entry(root, width=col2)

#combo
combo = ttk.Combobox(root, width=col2, values=["Done","Todo","Canceled"], state="readonly")
combo.set("Todo")
combo.bind('<<ComboboxSelected>>', lambda event: update_status(event.widget.get()))
    
def main():
    update_list()
    
    lbl0.grid(row=0,column=0)
    lb.grid(row=1,column=0)
    scroll.grid(row=1 ,column=1,sticky=tk.NS)
    btn.grid(row=2,column=0)
    
    lbl_status.grid(row=0,column=2)
    entry.grid(row=1,column=2)
    combo.grid(row=2,column=2)
    
    root.mainloop()

def add_note(name="new note"):
    global notes_count
    notes_count += 1
    if name == "new note":
        name += f" {notes_count}"
    notes.append(name)
    lb.insert(notes_count,name)
    lbl0.config(text=f"Notes: {notes_count}")

def open_note():
    pass
    
def update_list():
    for index,n in enumerate(notes):
        lb.insert(index,n)

def update_count():
    notes_count = len(notes)
    lbl0.config(text=f"Notes: {notes_count}")
    
def update_status(status):
    lbl_status.config(text=f"Status: {status}")
    
def int_parse(string):
    try:
        return int(string)
    except ValueError:
        return 0
    
main()