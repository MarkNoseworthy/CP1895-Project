from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class RecipeInformation(FlaskForm):
    recipe_name = StringField('Recipe Name:', validators=[DataRequired()])
    recipe_image = FileField('Recipe Image:', validators=[FileRequired()])
    ingredients_list = TextAreaField('List of Ingredients:', validators=[DataRequired()])
    prep_instructions = TextAreaField('Preparation Instructions:', validators=[DataRequired()])
    serving_instructions = StringField('Serving Instructions:', validators=[DataRequired()])
