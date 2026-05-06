from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import string
import random
import os
import qrcode

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)


# =========================
# DATABASE MODELS
# =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    qr_code = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


with app.app_context():
    db.create_all()


# =========================
# SHORT URL GENERATOR
# =========================

def generate_short_url():

    characters = string.ascii_letters + string.digits

    while True:

        short_url = ''.join(random.choices(characters, k=6))

        existing_url = URL.query.filter_by(short_url=short_url).first()

        if not existing_url:
            return short_url


# =========================
# QR CODE GENERATOR
# =========================

def generate_qr_code(short_url):

    full_url = f"http://127.0.0.1:5000/{short_url}"

    qr = qrcode.make(full_url)

    folder_path = "static/qr_codes"

    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{short_url}.png"

    file_path = os.path.join(folder_path, file_name)

    qr.save(file_path)

    return file_path


# =========================
# HOME PAGE
# =========================

@app.route('/', methods=['GET', 'POST'])
def index():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        original_url = request.form.get("url")

        if original_url:

            short_url = generate_short_url()

            qr_code_path = generate_qr_code(short_url)

            new_url = URL(
                original_url=original_url,
                short_url=short_url,
                qr_code=qr_code_path,
                user_id=session['user']
            )

            db.session.add(new_url)
            db.session.commit()

            flash("Short URL and QR Code generated successfully!", "success")

    all_urls = URL.query.filter_by(user_id=session['user']).all()

    return render_template(
        'index.html',
        all_urls=all_urls
    )


# =========================
# REDIRECT ROUTE
# =========================

@app.route('/<short_url>')
def redirect_url(short_url):

    url = URL.query.filter_by(short_url=short_url).first()

    if url:
        return redirect(url.original_url)

    flash("URL not found!", "danger")

    return redirect('/')


# =========================
# REGISTER
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:

            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash("Username already exists!", "danger")

            else:

                hashed_password = generate_password_hash(password)

                new_user = User(
                    username=username,
                    password=hashed_password
                )

                db.session.add(new_user)
                db.session.commit()

                flash("Registration successful! Please login.", "success")

                return redirect('/login')

    return render_template('register.html')


# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['user'] = user.id

            flash("Login successful!", "success")

            return redirect('/')

        else:
            flash("Invalid username or password!", "danger")

    return render_template('login.html')


# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('user', None)

    flash("Logged out successfully!", "info")

    return redirect('/login')


# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True)