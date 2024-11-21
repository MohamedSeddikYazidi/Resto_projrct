from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from datetime import timedelta
import os
import sqlite3

app = Flask(__name__)
app.secret_key = '0000'

# Durée de vie de la session : 1 minute
app.permanent_session_lifetime = timedelta(minutes=1)

# Assurer que Flask sert correctement les fichiers statiques depuis le dossier "static"
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('static', filename)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        #cursor.execute('DROP TABLE IF EXISTS users')  # Supprime la table existante
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        conn.commit()
        print("Database initialized successfully!")

# Initialiser la base de données au démarrage de l'application
init_db()

# Middleware pour vérifier la connexion
"""@app.before_request
def check_login():
    # Autoriser uniquement la connexion et l'enregistrement pour les non-connectés
    allowed_routes = ['login', 'register', 'serve_static_files']
    if 'user_id' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/commande')
def commande():
    return render_template('commande.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

"""@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupération des données du formulaire
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation des champs
        if not all([username, first_name, last_name, email, password, confirm_password]):
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        # Vérification de l'existence de l'email dans la base de données
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)', 
                               (username, first_name, last_name, email, password))
                conn.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Email already exists!", "danger")
                return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not all([email, password]):
            flash("All fields are required!", "danger")
            return redirect(url_for('login'))

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()

            if user:
                session.permanent = True  # Rend la session permanente
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash(f"Welcome, {user[1]}!", "success")
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password!", "danger")
                return redirect(url_for('login'))

    return render_template('login.html')

"""


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
