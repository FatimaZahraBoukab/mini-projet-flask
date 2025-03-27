from flask import Blueprint, render_template, session, redirect, url_for, flash, request, current_app
from models.user import User, LoginHistory, db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
import uuid

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('Vous devez vous connecter pour accéder à cette page', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    # Limiter à 3 dernières connexions pour le dashboard
    login_history = LoginHistory.query.filter_by(user_id=user.id).order_by(LoginHistory.login_date.desc()).limit(3).all()
    return render_template('dashboard.html', user=user, login_history=login_history)

@dashboard_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Vous devez vous connecter pour accéder à cette page', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update user information
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.telephone = request.form.get('telephone')
        user.adresse = request.form.get('adresse')
        
        # Check if password needs to be updated
        new_password = request.form.get('new_password')
        if new_password and len(new_password) >= 6:
            current_password = request.form.get('current_password')
            if user.check_password(current_password):
                user.set_password(new_password)
            else:
                flash('Le mot de passe actuel est incorrect', 'error')
                return redirect(url_for('dashboard.edit_profile'))
        
        try:
            db.session.commit()
            return redirect(url_for('dashboard.user_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour du profil: {str(e)}', 'error')
    
    return render_template('edit_profile.html', user=user)

@dashboard_bp.route('/profile/photo', methods=['POST'])
def update_profile_photo():
    if 'user_id' not in session:
        flash('Vous devez vous connecter pour accéder à cette page', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    if 'profile_photo' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('dashboard.edit_profile'))
    
    file = request.files['profile_photo']
    
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('dashboard.edit_profile'))
    
    if file:
        # Delete old profile photo if it exists
        if user.profile_photo:
            try:
                old_photo_path = os.path.join(current_app.root_path, 'static/uploads', user.profile_photo)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            except Exception as e:
                print(f"Error deleting old photo: {str(e)}")
        
        # Save new profile photo
        filename = secure_filename(file.filename)
        # Add unique identifier to prevent filename collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Ensure uploads directory exists
        uploads_dir = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        file_path = os.path.join(uploads_dir, unique_filename)
        file.save(file_path)
        
        # Update user profile photo in database
        user.profile_photo = unique_filename
        db.session.commit()
        
        
    
    return redirect(url_for('dashboard.user_dashboard'))

@dashboard_bp.route('/login-history')
def login_history():
    if 'user_id' not in session:
        flash('Vous devez vous connecter pour accéder à cette page', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    # Limiter à 10 dernières connexions pour la page d'historique
    login_history = LoginHistory.query.filter_by(user_id=user.id).order_by(LoginHistory.login_date.desc()).limit(10).all()
    
    return render_template('login_history.html', user=user, login_history=login_history)

