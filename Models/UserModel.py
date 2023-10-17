from Database.db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    ## Defin the user colubms. 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
    # Establishing the relationship with NotesModel (Backref simplies the creation of the reverse relationship).. Lazy controls how related objects are loaded and quired.
    notes = db.relationship('Models.NotesModel.NotesModel', backref='user', lazy=True)
    def __str__(self):  
        return str(self.json())

    def __repr__(self): 
        return self.__str__()

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'notes': [note.json() for note in self.notes]  # Including user notes in user JSON
        }
