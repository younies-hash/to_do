import json, os
from tkinter import Tk
import tkinter as tk
from notes import Todo
import settings

#theme
THEME= '#5865f2'
BACKGROUND = "#ffffff"
ACTIVE_THEME = '#4752c4'
NORMAL_TEXT_COLOR = '#33373e'
GHOST_TEXT_COLOR = '#a0a5af'
GHOST_TEXT = 'What needs to be done?'


todos = []
rows = []
todos_count = 0
selected_todo_index = None
auto_save_active = False
late_save = False #when  changing multiple todos at once lat_save tells the app to wait untill changes re finished before saving  all at once
completed = 0

FILE = 'todo.json'

root = Tk(screenName="Py-To-Do", className =" To-Do")
root.config(background=BACKGROUND)
root.geometry("350x400")


#menubar
menubar = tk.Menu(root)
root.config(menu=menubar)
#file
filemenu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Todo",command=lambda: add_todo(f'new todo {todos_count}'))
filemenu.add_command(label="Save",command=lambda: save())
filemenu.add_checkbutton(label="Auto Save",command=lambda: toggle_autosave())
filemenu.add_command(label="Settings",command=lambda: settings.setting_popup(root,lambda: refresh_ui()))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
# todo
editmenu = tk.Menu(menubar)
menubar.add_cascade(label="Todo", menu=editmenu)
editmenu.add_command(label="Check All", command=lambda: toggle_all(1))
editmenu.add_command(label="Uncheck All", command=lambda: toggle_all(0))
editmenu.add_command(label="Clear List", command=lambda: del_all())


#add note
input_frame = tk.Frame(root, bg=BACKGROUND)

entry = tk.Entry(input_frame, width=30, bd=4, relief=tk.FLAT, highlightthickness=2,highlightbackground='#cccccc', highlightcolor='#5865f2',fg = GHOST_TEXT_COLOR)

btn = tk.Button(input_frame, text="Add +",width=10,bd=4, relief=tk.FLAT, bg='#5865f2', fg='white', activebackground='#4752c4', activeforeground='white', command=lambda:add_todo(entry.get()))

#todo  list
scroll = tk.Scrollbar(root)
list_frame = tk.Frame(root, bg=BACKGROUND)
# scroll.config(command=list_frame.yview)

#footer
summery = tk.Label(list_frame, text=f"Completed: {completed} out of {todos_count}", bg=BACKGROUND, fg=THEME)

def main():
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    entry.bind('<Return>', lambda event: add_todo(entry.get()))
    root.bind('<Up>', lambda event: on_arrow(-1))
    root.bind('<Down>', lambda event: on_arrow(1))
    root.bind('<Delete>', on_del_key)
    root.bind('<space>', on_space_key)

    input_frame.pack(pady=10)
    entry.pack(side=tk.LEFT, padx=10, ipady=2)
    entry.insert(0, GHOST_TEXT)
    btn.pack(side=tk.RIGHT, padx=(0,10), ipady=1)
    
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, ipadx=40, expand=False)
    scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    
    summery.pack(side=tk.BOTTOM, fill=tk.X, padx=50)

    root.mainloop()

#add a new todo
def add_todo(name):
    if name == "" or name == GHOST_TEXT:
        return
    global todos_count
    new_todo = Todo(name)
    todos.append(new_todo)
    add_todo_wedgit(new_todo)
    todos_count += 1
    entry.delete(0, tk.END)
    refresh()
    autosave()

#show a new todo on screen
def add_todo_wedgit(todo):
    todo_row = tk.Frame(list_frame, bg=BACKGROUND)
    
    checkbox= tk.Checkbutton(todo_row, text=todo.title, variable=todo.status, onvalue=1,  offvalue=0, anchor="w", height=1, width=10, bg=BACKGROUND, fg=THEME, justify=tk.LEFT, wraplength=100,command=lambda: toggle(todo))
    
    x_btn = tk.Button(todo_row, text="X", width=2, height=1,bd=2,  relief=tk.FLAT, bg=BACKGROUND, fg='red', activebackground=ACTIVE_THEME, activeforeground=THEME, command=lambda: remove_todo(todo, todo_row))   
    
    checkbox.pack(side=tk.LEFT, fill=tk.X, padx=10, ipady=2,  ipadx=5,expand=True)
    x_btn.pack(side=tk.RIGHT, padx=(0,10), ipady=2)
    todo_row.pack(side=tk.TOP, fill=tk.X, padx=10, ipadx=25, expand=False)
    todo.wedgit = checkbox
    rows.append(todo_row)
  
#   key bindings
def select_todo(index):
    global selected_todo_index
    if selected_todo_index is not None:
        rows[selected_todo_index].config(bg=BACKGROUND)
        selected_todo_index = index
        rows[index].config(bg=ACTIVE_THEME)
    
def on_arrow(direction):
    if not rows:
        return
    global selected_todo_index
    if selected_todo_index is None:
        selected_todo_index=0
        select_todo(0)
    else:
        select_todo((selected_todo_index + direction) % len(rows))
    print(f"now selected: {selected_todo_index}")
        
def on_del_key(event):
    global selected_todo_index
    if selected_todo_index is not None:
        i = selected_todo_index
        remove_todo(todos[i], rows[i])
        
def on_space_key(event):
    global selected_todo_index
    if selected_todo_index is not None:
        i = selected_todo_index
        toggle(todos[i])


#check/uncheck todo  
def toggle(todo):
    global completed
    todo.toggle()
    todo.wedgit.toggle()
    print(f'toggling from the outside:  {todo.title} is now {todo.get_status()}')
    if todo.status.get()==1:
        completed += 1
    else:
        completed -= 1
    refresh()
    autosave()
    

#remove todo from list
def remove_todo(todo, widget):
    global todos_count
    global completed
    global selected_todo_index
    if selected_todo_index == todos.index(todo):
        rows.remove(rows[selected_todo_index])
        print(f"deleted: {selected_todo_index} now it's None")
        selected_todo_index = None
    if todo.status.get()==1:
        completed -= 1
    widget.destroy()
    todos.remove(todo)
    todos_count -= 1
    refresh()
    autosave()

# rename todo
# unimplemented
def edit_todo(todo):
    # TODO: implement
    return

#update the summery/footer
def refresh():
    global completed
    global todos_count
    if completed < 0:
        completed = 0
    if todos_count < 0:
        todos_count = 0
    summery.config(text=f"Completed: {completed} out of {todos_count}")

# unimplemented
def refresh_ui(ui_settings):
    return

# change all todos
def toggle_all(val):
    global late_save
    late_save = True
    for todo in todos:
        if todo.status.get() != val:
            toggle(todo)
    late_save = False
    autosave()

def del_all():
    global todos_count
    global completed
    global selected_todo_index
    global late_save
    late_save = True
    todos.clear()
    for wedgit in rows:
        wedgit.destroy()
    rows.clear()
    selected_todo_index = None
    todos_count=0
    completed=0
    refresh()
    late_save = False
    autosave()

#remove ghost text from entry
def on_focus_in(event):
    if entry.get() == GHOST_TEXT:
        entry.delete(0, tk.END)
        entry.config(fg=NORMAL_TEXT_COLOR)

#add ghost text back to entry
def on_focus_out(event):
    if entry.get() == "":
        entry.config(fg=GHOST_TEXT_COLOR)
        entry.insert(0, GHOST_TEXT)

# unused
def int_parse(string):
    try:
        return int(string)
    except ValueError:
        return 0
    
def save():
    with open(FILE, 'w') as f:
        json.dump([t.to_dict() for t in todos], f, indent=2)

def autosave():
    global late_save
    if auto_save_active:
        if not late_save:
            save()

def load():
    global todos
    if os.path.exists(FILE):
        with open(FILE) as f:
            todos = [Todo.from_dict(t) for t in json.load(f)]
            del_all()
            for todo in todos:
                add_todo(todo.title)

def toggle_autosave():
    global auto_save_active
    auto_save_active = not auto_save_active

#
main()