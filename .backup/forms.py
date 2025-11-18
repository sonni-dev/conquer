from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField, DateTimeField, RadioField
from wtforms.validators import InputRequired, Optional
from app import db
from app.models import TaskTemplate, SubTask, TaskInstance, SubTaskCompletion


# CREATE FORMS

class NewTaskTemplateForm(FlaskForm):
    title = StringField("Task Title*", validators=[InputRequired()])
    category = RadioField("Category*",
                          choices=[
                              ('cleaning', 'Cleaning'),
                              ('self-care', 'Self-Care'),
                              ('doby', 'Doby'),
                              ('work', 'Work'),
                              ('errands', 'Errands'),
                              ('social', 'Social'),
                              ('coding', 'Coding / Personal Projects'),
                              ('adulting', 'Adulting')
                          ], coerce=str)
    task_type
    effort_type
    location_type
    base_xp_low
    base_xp_medium
    base_xp_high

