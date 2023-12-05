from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    filedata = FileField('File', validators=[DataRequired()])
    on_display_at = SelectField('Output mode',
                                choices=[('highlight', 'Full document with highlights'),
                                         ('sectioned', 'Portions of the document')])
    submit = SubmitField('Add parameters')
