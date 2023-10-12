import logging
from Models.NotesModel import NotesModel
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
    def get_notes():
        try: 
            all_notes = NotesModel.query.all()
            if not all_notes:
                raise Exception("No notes found in the database")
            notes_json = [notes.json() for notes in all_notes], 
            return jsonify({'message': notes_json})
        except Exception as error:
            print(error)
            return jsonify({'error': str(error)}), 400
