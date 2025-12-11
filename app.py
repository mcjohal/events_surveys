from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'santa-secret-2025'  # For flash messages—change in prod

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace(
    "postgres://", "postgresql://"
) if 'DATABASE_URL' in os.environ else 'sqlite:///surveys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Survey Model
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100))
    color = db.Column(db.String(50))
    hobbies = db.Column(db.String(200))
    drink = db.Column(db.String(100))
    candy = db.Column(db.String(100))
    salty = db.Column(db.String(100))
    baked = db.Column(db.String(100))
    fastfood = db.Column(db.String(100))
    movie = db.Column(db.String(100))
    book = db.Column(db.String(100))
    shop = db.Column(db.String(100))
    team = db.Column(db.String(100))
    other = db.Column(db.String(200))
    sweet_salty = db.Column(db.String(20))
    choc_candy = db.Column(db.String(20))
    mints_gum = db.Column(db.String(20))
    colors = db.Column(db.String(20))
    music_pod = db.Column(db.String(20))
    book_movie = db.Column(db.String(20))
    stay_go = db.Column(db.String(20))
    bird_owl = db.Column(db.String(20))
    chap_lip = db.Column(db.String(20))
    dogs_cats = db.Column(db.String(20))
    giftcards = db.Column(db.String(3))
    food = db.Column(db.String(3))
    clothing = db.Column(db.String(3))
    decor = db.Column(db.String(3))
    plants = db.Column(db.String(3))
    allergies = db.Column(db.String(200))
    want = db.Column(db.Text)
    dontwant = db.Column(db.Text)
    shirt = db.Column(db.String(10))
    pant = db.Column(db.String(10))
    shoe = db.Column(db.String(10))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

PASSWORD = 'santa2025'  # Change this to your desired password

def get_all_surveys():
    return db.session.query(Survey).all()

@app.route('/')
def index():
    surveys = get_all_surveys()
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
            # Create new survey
            form_dict = {k: v for k, v in request.form.items() if k != 'password'}
            new_survey = Survey(
                name=form_dict.get('name'),
                color=form_dict.get('color'),
                hobbies=form_dict.get('hobbies'),
                drink=form_dict.get('drink'),
                candy=form_dict.get('candy'),
                salty=form_dict.get('salty'),
                baked=form_dict.get('baked'),
                fastfood=form_dict.get('fastfood'),
                movie=form_dict.get('movie'),
                book=form_dict.get('book'),
                shop=form_dict.get('shop'),
                team=form_dict.get('team'),
                other=form_dict.get('other'),
                sweet_salty=form_dict.get('sweet_salty'),
                choc_candy=form_dict.get('choc_candy'),
                mints_gum=form_dict.get('mints_gum'),
                colors=form_dict.get('colors'),
                music_pod=form_dict.get('music_pod'),
                book_movie=form_dict.get('book_movie'),
                stay_go=form_dict.get('stay_go'),
                bird_owl=form_dict.get('bird_owl'),
                chap_lip=form_dict.get('chap_lip'),
                dogs_cats=form_dict.get('dogs_cats'),
                giftcards=form_dict.get('giftcards'),
                food=form_dict.get('food'),
                clothing=form_dict.get('clothing'),
                decor=form_dict.get('decor'),
                plants=form_dict.get('plants'),
                allergies=form_dict.get('allergies'),
                want=form_dict.get('want'),
                dontwant=form_dict.get('dontwant'),
                shirt=form_dict.get('shirt'),
                pant=form_dict.get('pant'),
                shoe=form_dict.get('shoe')
            )
            db.session.add(new_survey)
            db.session.commit()
            flash('Survey added successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('survey.html', error=error, form_data=form_data)

@app.route('/edit/<int:survey_id>', methods=['GET', 'POST'])
def edit_survey(survey_id):
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash('Survey not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Update the existing survey (no password check for edit)
        form_dict = {k: v for k, v in request.form.items() if k != 'password'}
        for key, value in form_dict.items():
            if hasattr(survey, key):
                setattr(survey, key, value)
        survey.timestamp = datetime.utcnow()
        db.session.commit()
        flash('Survey updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # Pass survey data as form_data for pre-fill
    form_data = survey.to_dict()
    form_data['id'] = survey_id  # For any ID needs
    return render_template('edit.html', form_data=form_data, survey_id=survey_id)

@app.route('/delete/<int:survey_id>')
def delete_survey(survey_id):
    survey = db.session.get(Survey, survey_id)
    if survey:
        db.session.delete(survey)
        db.session.commit()
        flash('Survey deleted successfully!', 'success')
    else:
        flash('Survey not found!', 'error')
    return redirect(url_for('index'))

@app.route('/view/<int:survey_id>')
def view_survey(survey_id):
    survey = db.session.get(Survey, survey_id)
    if survey:
        return render_template('view.html', survey=survey)
    flash('Survey not found!', 'error')
    return redirect(url_for('index'))

# Create tables on first run (for local dev; Render will handle via env)
with app.app_context():
    db.create_all()

@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
    return "DB tables created!"

if __name__ == '__main__':
    app.run(debug=True)