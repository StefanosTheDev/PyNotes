from Database.db import db

class NotesModel(db.Model):
    __tablename__ = 'notes'  # Correcting table name
    
    notes_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100000), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Creating foreign key
    
    def __str__(self):  
        return str(self.json())

    def __repr__(self): 
        return self.__str__()

    def json(self):
        return {
            'notes_id': self.notes_id,
            'content': self.content,
            'user_id': self.user_id  # Including user_id in note JSON
        }