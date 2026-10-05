
from tkinter import IntVar

class Todo:
    
    wedgit=None
    
    def __init__(self, title):
        self.title = title
        self.status = IntVar(value=0)
        
    def get_status(self):
        if self.status.get() == 1:
            return "Done"
        else:
            return "Todo"

    def toggle(self):
        self.status.set(1 if self.status.get() == 0 else 0)
        print(f'toggling from the inside:  {self.title} is now {self.get_status()}')
        
    def to_dict(self):
        return {'title': self.title, 'status': self.status.get()}
    
    @classmethod
    def from_dict(self, data):
        self.title = data['title']
        self.status.set(data['status'])
    
    def __str__(self):
        return f"Title: {self.title}\nStatus: {self.get_status()}"
