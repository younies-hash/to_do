
class Note:
    def __init__(self, title):
        self.title = title
        self.content = ''

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}"