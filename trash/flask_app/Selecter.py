from flask import Flask, render_template, request, redirect, url_for
import json
import random
import time

app = Flask(__name__)

filename = 'names_web.json'

# Function to load names from the JSON file
def load_names():
    try:
        with open(filename, 'r') as file:
            names = json.load(file)
        return names
    except FileNotFoundError:
        return []

# Function to save names to the JSON file
def save_names(names):
    with open(filename, 'w') as file:
        json.dump(names, file, indent=2)

# Function to select a random name
def select_random_name(names):
    if not names:
        return None

    return random.choice(names)

# Function to ask the user if they appreciate the presented name
def ask_user_preference(name):
    return name if request.form.get('appreciate') == 'yes' else None

# Main route
@app.route('/')
def index():
    names = load_names()
    selected_name = select_random_name(names)
    
    # Pass the remaining names to the template
    remaining_names = names.copy()
    remaining_names.remove(selected_name) if selected_name in remaining_names else None
    
    return render_template('index.html', selected_name=selected_name, remaining_names=remaining_names)


# Post route to handle form submission
@app.route('/result', methods=['POST'])
def result():
    selected_name = request.form['selected_name']
    appreciated_name = ask_user_preference(selected_name)

    if appreciated_name:
        names = load_names()
        names.remove(appreciated_name)
        save_names(names)
        return render_template('result.html', result=f"Nydelig valgt! {appreciated_name} Kan trekke en gave!")
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
