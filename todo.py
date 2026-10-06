
from tkinter import IntVar

class Todo:
    def __init__(self, title):
        self.title = title
        self.status = IntVar(value=0)
        self.widget=None
        
    def get_status(self):
        if self.status.get() == 1:
            return "Done"
        else:
            return "Todo"

    # clicking on acheckbox does this automatically, only use this when we need to toggle manually from somewhere else, or use todo.widget.toggle()
    def toggle(self):
        self.status.set(1 if self.status.get() == 0 else 0)
        
    def to_dict(self):
        return {'title': self.title, 'status': self.status.get()}
    
    @classmethod
    def from_dict(cls, data):
        todo = cls(data['title'])
        todo.status.set(data['status'])
        return todo
    
    def __str__(self):
        return f"Title: {self.title}\nStatus: {self.get_status()}"
