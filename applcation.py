import os
from flask import Flask, redirect, url_for, request, render_template
import pandas as pd
from werkzeug.utils import secure_filename
from forms import RecipeInformation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dslgjheriout94g34uth98hbrgsgo34t98gherihg934hg'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/search_recipe', methods = ['POST', 'GET'])
def search_recipe():
    return render_template('search_recipe.html')

@app.route('/add_recipe', methods = ['POST', 'GET'])
def add_recipe():
    if request.method == 'POST':
        dish_name = request.form['dish_name']
        print(dish_name)
        return "Dish added successfully."
    else:
        return render_template('add_recipe_manual.html')

@app.route('/add_recipe_auto', methods = ['POST', 'GET'])
def add_recipe_auto():
    form = RecipeInformation()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        pic_filename = recipe_name.lower().replace(" ", "_") + '.' + secure_filename(form.recipe_image.data.filename).split('.')[-1]
        form.recipe_image.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        ingredients_list = form.ingredients_list.data
        prep_instructions = form.prep_instructions.data
        serving_instructions = form.serving_instructions.data
        df = pd.DataFrame([{'dish': recipe_name, 'pic': pic_filename, 'ingredients': ingredients_list, 'prep': prep_instructions, 'serving': serving_instructions}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return redirect(url_for('base'))
    else:
        return render_template('add_recipe_auto.html', form=form)

@app.route('/remove_recipe', methods = ['POST', 'GET'])
def remove_recipe():
    form = RecipeInformation()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        df = pd.DataFrame([{'dish': recipe_name}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return redirect(url_for('base'))
    else:
        return render_template('remove_recipe.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)