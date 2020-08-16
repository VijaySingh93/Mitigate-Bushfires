from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


class report(FlaskForm):
    name = StringField('',validators=[DataRequired()])
    region = StringField('',validators=[DataRequired()])
    phone = StringField('',validators=[DataRequired()])
    image = FileField('Select file',
                             validators=[FileRequired('File was empty!')])
    submit = SubmitField('Report')