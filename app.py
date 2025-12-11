from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'surveys.json'
PASSWORD = 'santa2025'  # Change this to your desired password

def load_surveys():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_surveys(surveys):
    with open(DATA_FILE, 'w') as f:
        json.dump(surveys, f, indent=4)

@app.route('/')
def index():
    surveys = load_surveys()
    return render_template('index.html', surveys=surveys)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    error = None
    form_data = {}
    if request.method == 'POST':
        password = request.form.get('password')
        if password != PASSWORD:
            error = "Invalid password! Ho ho no—try again."
            form_data = {k: v for k, v in request.form.items() if k != 'password'}
        else:
            # Remove password from form data before saving
            form_data = {k: v for k, v in request.form.items() if k != 'password'}
            data = {
                'id': len(load_surveys()) + 1,
                'timestamp': datetime.now().isoformat(),
                **form_data
            }
            surveys = load_surveys()
            surveys.append(data)
            save_surveys(surveys)
            return redirect(url_for('index'))
    return render_template('survey.html', error=error, form_data=form_data)

@app.route('/view/<int:survey_id>')
def view_survey(survey_id):
    surveys = load_surveys()
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    if survey:
        return render_template('view.html', survey=survey)
    return "Survey not found", 404

if __name__ == '__main__':
    app.run(debug=True)