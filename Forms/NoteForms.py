from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, SubmitField

class NoteForm(FlaskForm):
    content = TextAreaField('Content', [validators.Length(min=1)], render_kw={"rows": 10, "cols": 11})
    submit = SubmitField('Create Note')

class GPTForm(FlaskForm):
    Gpt = SubmitField('GPT Integration')

class DeleteForm(FlaskForm):
    #note_id = TextAreaField('ID:')
    delete = SubmitField('Confirm Deletion')
    cancel = SubmitField('Cancel Deletion')