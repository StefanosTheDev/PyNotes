import logging
from Models.NotesModel import NotesModel
from Models.UserModel import UserModel
from flask import jsonify, session 
from Database.db import db
from sqlalchemy.exc import IntegrityError, OperationalError
import warnings

class NotesService:
    def create_note(content, user_id):
        try:
            create_note = NotesModel(content=content, user_id=user_id)
            db.session.add(create_note)
            db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Could no add {create_note} to the database")
            db.session.rollback()
            raise
    #**
    # Get the user ID from the session. If there is not a session ID say there is none and you cant make a request.
    # If a User ID Session exists. Query for all the notes and return them first as a console. 
    # Once completed. Then Update the Jinja Templates. 
    def get_notes():
        try:
        # Check if the user is logged in and if a user ID exists in the session
            if session.get('logged_in') == True and 'user_id' in session:
                user_id = session['user_id']
                user = UserModel.query.filter_by(id=user_id).first()
            
                if user:
                    user_notes = user.notes
                    return user_notes
                else:
                    print("User not found.")

        except Exception as e:
            logging.error(e)
            raise
    def delete_note():
        pass