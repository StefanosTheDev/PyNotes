from flask import request, render_template, jsonify, redirect, url_for, flash, Blueprint, session

from functools import wraps
from Services.NotesService import NotesService
from Forms.NoteForms import NoteForm
from GlobalExceptions.ServiceException import ServiceException, UsernameError, PasswordError
note_blueprint = Blueprint('notes', __name__)

@note_blueprint.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    form = NoteForm()

    try:
        if form.validate_on_submit():
            content = form.content.data
            
            # Retrieve user_id from the session #
            user_id = session.get('user_id')
            if user_id is None:
                flash("User not logged in", "danger")
                return render_template('Notes/Notes.html')
            
            createdNote = NotesService.create_note(content, user_id=user_id)
            
            if createdNote:
                flash("Note Created Successfully", "success")
                return render_template('Notes/Notes.html')
    except Exception as e:
        print(f"Unexpected error {str(e)}")
        flash(f"An unexpected error occured. Please Try again", "danger")
        return render_template('Notes/Notes.html')
    return render_template('Notes/AddNotes.html', form=form)
    
@note_blueprint.route('/notes/getNotes', methods=['GET'])
def get_notes():
     return NotesService.get_notes()