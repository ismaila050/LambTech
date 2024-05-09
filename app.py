from flask import Flask, request, render_template, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
import random

app = Flask(__name__)
app.secret_key = 'kharal_ma_tester_nakh_dina_bakh'  # Clé secrète pour les sessions (à remplacer)

# Configuration SMTP de Gmail (remplacez les valeurs par vos propres informations)
gmail_user = 'anniediouf2812@gmail.com'
gmail_password = 'P@sser1234567389'

# Base de données simplifiée pour stocker les informations d'authentification (à remplacer par une vraie base de données)
users = {
    'annemariediouf39@gmail.com': {
        'password': 'password123',
        'email': 'annemariediouf39@gmail.com'
    }
}

# Fonction pour générer un code de vérification à 6 chiffres
def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# Fonction pour envoyer le code de vérification par e-mail
def send_verification_code(email, verification_code):
    try:
        msg = MIMEText(f'Votre code de vérification est : {verification_code}')
        msg['Subject'] = 'Code de vérification'
        msg['From'] = gmail_user
        msg['To'] = email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False

# Route pour la page d'authentification et le traitement du formulaire
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and password == users[email]['password']:
            # Authentification réussie, génération et envoi du code de vérification par e-mail
            verification_code = generate_verification_code()
            if send_verification_code(email, verification_code):
                session['username'] = email
                session['verification_code'] = verification_code
                return redirect(url_for('verify'))
            else:
                return "Une erreur s'est produite lors de l'envoi du code de vérification par e-mail."
        else:
            return 'Échec de l\'authentification. Vérifiez vos informations de connexion.'
    else:
        return render_template('login.html')
    
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route pour la vérification du code de vérification
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'username' not in session or 'verification_code' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session['username']
        verification_code = request.form['verification_code']
        if verification_code == session['verification_code']:
            return f'Bienvenue, {username} ! Authentification réussie.'
        else:
            return 'Échec de l\'authentification. Le code de vérification est incorrect.'
    else:
        return render_template('verification.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
