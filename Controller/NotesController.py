from flask import request, render_template, jsonify, redirect, url_for, flash, Blueprint, session

from functools import wraps
from Services.NotesService import NotesService
from Forms.NoteForms import NoteForm, GPTForm, DeleteForm
from GlobalExceptions.ServiceException import ServiceException, UsernameError, PasswordError
note_blueprint = Blueprint('notes', __name__)

@note_blueprint.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    form = NoteForm()
    gptForm = GPTForm()
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
                flash("Note Created Succesfully", "success")
                return redirect(url_for('notes.get_notes'))
    except Exception as e:
        print(f"Unexpected error {str(e)}")
        flash(f"An unexpected error occured. Please Try again", "danger")
        return render_template('Notes/Notes.html')
    return render_template('Notes/AddNotes.html', form=form, gptForm=gptForm)
    
@note_blueprint.route('/notes/getNotes', methods=['GET'])
def get_notes():
    notes = NotesService.get_notes()
    return render_template('Notes/Notes.html', notes=notes)

@note_blueprint.route('/notes/delete/note', methods=['GET', 'POST'])
def delete_note():
    form = DeleteForm()
    try:
        note_id = request.form.get('notes_id') ## how to get note from the form.
        clicked_button = request.form.get('delete')
        print(note_id)
        if clicked_button == 'delete':
            print(note_id)
            print('Delete was clicked')
            pass
        elif clicked_button == 'cancel':
            ## perform cancelation features
            pass
        
    except Exception as e:
        flash(f"{e}", 'danger')
        return render_template('Note/Notes.html', form=form)
    
    return render_template('Notes/DeleteNote.html', form=form)