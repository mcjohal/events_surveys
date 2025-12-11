from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'santa-secret-2025'  # For flash messages—change in prod

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
            flash('Survey added successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('survey.html', error=error, form_data=form_data)

@app.route('/edit/<int:survey_id>', methods=['GET', 'POST'])
def edit_survey(survey_id):
    surveys = load_surveys()
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    if not survey:
        flash('Survey not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Update the existing survey (no password check for edit)
        update_data = {k: v for k, v in request.form.items() if k != 'password'}
        for s in surveys:
            if s['id'] == survey_id:
                s.update(update_data)
                s['timestamp'] = datetime.now().isoformat()  # Update timestamp
                break
        save_surveys(surveys)
        flash('Survey updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # Pass survey data as form_data for pre-fill
    return render_template('edit.html', form_data=survey, survey_id=survey_id)

@app.route('/delete/<int:survey_id>')
def delete_survey(survey_id):
    surveys = load_surveys()
    original_count = len(surveys)
    surveys = [s for s in surveys if s['id'] != survey_id]
    if len(surveys) < original_count:
        save_surveys(surveys)
        flash('Survey deleted successfully!', 'success')
    else:
        flash('Survey not found!', 'error')
    return redirect(url_for('index'))

@app.route('/view/<int:survey_id>')
def view_survey(survey_id):
    surveys = load_surveys()
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    if survey:
        return render_template('view.html', survey=survey)
    flash('Survey not found!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)