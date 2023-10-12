from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, SubmitField

class NoteForm(FlaskForm):
    content = TextAreaField('Content', [validators.Length(min=1)], render_kw={"rows": 10, "cols": 11})
    submit = SubmitField('Create Note')