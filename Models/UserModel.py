# AdminModel.py
from Database.db import db  # Assuming app.py and AdminModel.py are in the same directory

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Consider hashing the password!
    role = db.Column(db.String(50), nullable=False)

    def __str__(self):  
        return str(self.json())

    def __repr__(self): 
        return self.__str__()

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,  # Ideally you'd never print or share this
            'role': self.role
        }
