import json, os
from tkinter import Tk
import tkinter as tk
from todo import Todo
import tkinter.font as tkfont

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
config = {'auto_save': False, 'auto_load': False}
late_save = False #when  changing multiple todos at once lat_save tells the app to wait untill changes re finished before saving  all at once
completed = 0
last_width = [0]

FILE = 'todo.json' #save file
CONFIG_FILE = 'config.json' #config file


def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config.update(json.load(f))
load_config()

root = Tk(screenName="Py-To-Do", className =" To-Do")
root.config(background=BACKGROUND)
root.geometry("350x400")
root.minsize(350, 400)

title_font = tkfont.Font(family='Helvetica', size=4, weight='bold')
todo_font = tkfont.Font(family='Helvetica', size=3)

auto_save_var = tk.BooleanVar(value=config['auto_save'])
auto_load_var = tk.BooleanVar(value=config['auto_load'])
#menubar
menubar = tk.Menu(root, font=todo_font,)
root.config(menu=menubar)
#file
filemenu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Save",command=lambda: save())
filemenu.add_checkbutton(label="Auto Save",command=lambda: reconfig('auto_save'), variable=auto_save_var)
filemenu.add_command(label="Load",command=lambda: load())
filemenu.add_checkbutton(label="Auto Load",command=lambda: reconfig('auto_load'), variable=auto_load_var)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
# todo
editmenu = tk.Menu(menubar)
menubar.add_cascade(label="Todo", menu=editmenu)
editmenu.add_command(label="Check All", command=lambda: toggle_all(1))
editmenu.add_command(label="Uncheck All", command=lambda: toggle_all(0))
editmenu.add_command(label="Clear List", command=lambda: del_all())


#interface for adding todos
input_frame = tk.Frame(root, bg=BACKGROUND)

entry = tk.Entry(input_frame, font=todo_font, width=30, bd=4, relief=tk.FLAT, highlightthickness=2,highlightbackground='#cccccc', highlightcolor='#5865f2',fg = GHOST_TEXT_COLOR)

btn = tk.Button(input_frame, font=todo_font, text="Add +",width=10,bd=4, relief=tk.FLAT, bg='#5865f2', fg='white', activebackground='#4752c4', activeforeground='white', command=lambda:add_todo(entry.get()))

#todo  list
scroll = tk.Scrollbar(root)
list_frame = tk.Frame(root, bg=BACKGROUND)

#footer
summery = tk.Label(list_frame, font=todo_font, text=f"Completed: {completed} out of {todos_count}", bg=BACKGROUND, fg=THEME)

def main():
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    entry.bind('<Return>', lambda event: add_todo(entry.get()))
    root.bind('<Up>', lambda event: on_arrow(-1))
    root.bind('<Down>', lambda event: on_arrow(1))
    root.bind('<Delete>', on_del_key)
    root.bind('<space>', on_space_key)
    root.bind('<Configure>', resize)

    input_frame.pack(pady=10)
    entry.pack(side=tk.LEFT, padx=10, ipady=2, fill=tk.X)
    entry.insert(0, GHOST_TEXT)
    btn.pack(side=tk.RIGHT, padx=(0,10), ipady=1, fill=tk.X)
    
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, ipadx=40, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    
    summery.pack(side=tk.BOTTOM, fill=tk.X, padx=50)
    
    if config['auto_load']:
        load()
    root.mainloop()

#add a new todo
def add_todo(name):
    if name == "" or name == GHOST_TEXT:
        return
    global todos_count
    new_todo = Todo(name)
    todos.append(new_todo)
    add_todo_widget(new_todo)
    todos_count += 1
    entry.delete(0, tk.END)
    refresh()
    autosave()

#show a new todo on screen
def add_todo_widget(todo):
    todo_row = tk.Frame(list_frame, bg=BACKGROUND)
    
    checkbox= tk.Checkbutton(todo_row, font=todo_font, text=todo.title, variable=todo.status, onvalue=1,  offvalue=0, anchor="w", height=1, width=10, bg=BACKGROUND, fg=THEME, justify=tk.LEFT, wraplength=100,command=lambda: toggle(todo))
    
    x_btn = tk.Button(todo_row, font=todo_font, text="X", width=2, height=1,bd=2,  relief=tk.FLAT, bg=BACKGROUND, fg='red', activebackground=ACTIVE_THEME, activeforeground=THEME, command=lambda: remove_todo(todo, todo_row))   
    
    checkbox.pack(side=tk.LEFT, fill=tk.X, padx=10, ipady=2,  ipadx=5,expand=True)
    x_btn.pack(side=tk.RIGHT, padx=(0,10), ipady=2)
    todo_row.pack(side=tk.TOP, fill=tk.X, padx=10, ipadx=25, expand=False)
    todo.widget = checkbox
    rows.append(todo_row)
  
# key bindings
def select_todo(index):
    global selected_todo_index
    if selected_todo_index is not None:
        rows[selected_todo_index].config(bg=BACKGROUND)
    selected_todo_index = index
    rows[index].config(bg=ACTIVE_THEME) # TODO:change this
    print(f"now selected: {selected_todo_index}")
    
def on_arrow(direction):
    if not rows:
        return
    global selected_todo_index
    if selected_todo_index is None:
        selected_todo_index=0
        select_todo(0)
    else:
        select_todo((selected_todo_index + direction) % len(rows))
        
def on_del_key(event):
    global selected_todo_index
    if selected_todo_index is not None:
        if selected_todo_index < len(rows):
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
    select_todo(todos.index(todo))
    if todo.status.get()==1:
        completed += 1
    else:
        completed -= 1
    refresh()
    autosave()

#remove todo from list
def remove_todo(todo, widget):
    global todos_count, completed, selected_todo_index
    
    index = todos.index(todo)
    
    if selected_todo_index is not None:
        if selected_todo_index == index:
            selected_todo_index = None
        elif selected_todo_index > index:
            selected_todo_index -= 1
    if todo.status.get()==1:
        completed -= 1
        
    rows.remove(rows[index])
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

def resize(event):
    if event.widget is not root:
        return
    width = event.width
    if abs(width - last_width[0]) < 20:
        return
    last_width[0] = width
    title_font.configure(size=max(4, width//24))
    todo_font.configure(size=max(3, width//38))
    for todo in todos:
        todo.widget.config(font=todo_font, wraplength=width-90)

# change all todos
def toggle_all(val):
    global late_save
    late_save = True
    for todo in todos:
        if todo.status.get() != val:
            todo.widget.toggle() # don't call todo.toggle() here, todo.status changes automatically here
    late_save = False
    autosave()

def del_all():
    global todos_count
    global completed
    global selected_todo_index
    global late_save
    late_save = True
    todos.clear()
    for widget in rows:
        widget.destroy()
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
    if config['auto_save']:
        if not late_save:
            save()

def load():
    global todos_count, completed
    if not os.path.exists(FILE):
        return
    with open(FILE) as f:
        data = json.load(f)
    for d in data:
        todo = Todo.from_dict(d)
        todos.append(todo)
        add_todo_widget(todo)
        todos_count += 1
        completed += todo.status.get()
    autosave()

def reconfig(setting):
    config[setting] = not config[setting]
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

#
main()