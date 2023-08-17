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

@app.route('/search_recipe', methods = ['GET'])
def search_recipe():
    return render_template('search_recipe.html')

@app.route('/search_recipe_results', methods=['GET'])
def search_recipe_results():
    search_term = request.args.get('search_term', '')
    matched_recipes = []

    if search_term:
        csv_files = [filename for filename in os.listdir(app.config['SUBMITTED_DATA']) if filename.endswith('.csv')]

        for csv_filename in csv_files:
            csv_path = os.path.join(app.config['SUBMITTED_DATA'], csv_filename)
            df = pd.read_csv(csv_path)

            if 'dish' in df.columns and search_term.lower() in df['dish'].str.lower().values:
                matched_recipes.append({'csv_filename': csv_filename, 'recipe_name': df.at[0, 'dish'],
                                        'ingredients': df.at[0, 'ingredients'], 'prep': df.at[0, 'prep'],
                                        'serving': df.at[0, 'serving'], 'pic': df.at[0, 'pic']})

    return render_template('search_recipe_results.html', search_term=search_term, matched_recipes=matched_recipes)

@app.route('/view_all_recipes', methods=['GET'])
def view_all_recipes():
    recipes = get_all_recipes()
    return render_template('view_all_recipes.html', recipes=recipes)

def get_all_recipes():
    data_dir = app.config['SUBMITTED_DATA']
    csv_files = [filename for filename in os.listdir(data_dir) if filename.endswith('.csv')]

    all_recipes = []
    for csv_filename in csv_files:
        csv_path = os.path.join(data_dir, csv_filename)
        df = pd.read_csv(csv_path)
        recipe_info = {
            'recipe_name': df.at[0, 'dish'],
            'ingredients': df.at[0, 'ingredients'],
            'prep': df.at[0, 'prep'],
            'serving': df.at[0, 'serving'],
            'pic': df.at[0, 'pic']
        }
        all_recipes.append(recipe_info)

    return all_recipes


# @app.route('/add_recipe', methods = ['POST', 'GET'])
# def add_recipe():
#     if request.method == 'POST':
#         dish_name = request.form['dish_name']
#         print(dish_name)
#         return "Dish added successfully."
#     else:
#         return render_template('add_recipe_manual.html')

@app.route('/add_recipe_auto', methods = ['POST', 'GET'])
def add_recipe_auto():
    form = RecipeInformation()
    if form.validate():
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


@app.route('/remove_recipe', methods=['GET', 'POST'])
def remove_recipe():
    if request.method == 'POST':
        recipe_to_remove = request.form['recipe_to_remove']
        csv_filename = recipe_to_remove.lower().replace(" ", "_") + '.csv'
        csv_path = os.path.join(app.config['SUBMITTED_DATA'], csv_filename)

        if os.path.exists(csv_path):
            os.remove(csv_path)
        return redirect(url_for('remove_recipe'))

    recipes = get_recipe_list()
    return render_template('remove_recipe.html', recipes=recipes)

def get_recipe_list():
    csv_files = [filename for filename in os.listdir(app.config['SUBMITTED_DATA']) if filename.endswith('.csv')]

    recipe_list = []
    for csv_filename in csv_files:
        recipe_name = csv_filename.replace('.csv', '').replace('_', ' ').title()
        recipe_list.append(recipe_name)

    return recipe_list


if __name__ == '__main__':
    app.run(debug=True)