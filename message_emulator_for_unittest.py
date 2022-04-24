class User():
    def __init__(self, user_id, first_name, last_name):
        self.id: int = user_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        
class Message():
    def __init__(self, from_user, date, text):
        self.from_user: User = from_user
        self.date: int = date
        self.text = text
