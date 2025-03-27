from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models.user import db, User
from config import Config
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User, LoginHistory, db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        telephone = request.form['telephone']
        adresse = request.form['adresse']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Vérification des mots de passe
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return redirect(url_for('auth.register'))
        
        # Gestion de la photo de profil
        profile_photo = None
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(file_path)
                profile_photo = filename
        
        # Vérification si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Ce nom d\'utilisateur existe déjà', 'error')
            return redirect(url_for('auth.register'))
        
        # Hachage du mot de passe
        hashed_password = generate_password_hash(password)
        
        # Création de l'utilisateur
        new_user = User(
            username=username, 
            email=email, 
            telephone=telephone, 
            adresse=adresse, 
            password=hashed_password,
            profile_photo=profile_photo
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie ! Connectez-vous maintenant.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()




        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id

             # Record login history
            login_history = LoginHistory(
                user_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db.session.add(login_history)
            db.session.commit()

    
            return redirect(url_for('dashboard.user_dashboard'))
        else:
            flash('Identifiants incorrects', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
  
    return redirect(url_for('auth.login'))





