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
        if request.method == 'POST':
            note_id = session.get('current_note_id')  # Retrieve the note_id from the session.
            clicked_button = request.form.get('action')  # Get the value of the clicked button.

            if clicked_button == 'delete':
                if note_id is not None:
                    NotesService.delete_note(note_id)
                    flash(f"Note Deleted Successfully: {note_id}", 'success')
                    session.pop('current_note_id', None)  # Remove the note_id from the session after processing.
                    return redirect(url_for('notes.get_notes'))
                else:
                    flash("Note ID not found.", 'danger')
            elif clicked_button == 'cancel':
                flash("Note deletion canceled.", 'info')
        elif request.method == 'GET':
                note_id = request.args.get('notes_id')
                session['current_note_id'] = note_id
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    
    return render_template('Notes/DeleteNote.html', form=form, note_id=session.get('current_note_id'))
