from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from supabase import create_client
from .models.user import User
import json

main = Blueprint('main', __name__)

def get_supabase():
    return create_client(
        current_app.config['SUPABASE_URL'],
        current_app.config['SUPABASE_KEY']
    )

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password')
            return redirect(url_for('main.login'))
        
        supabase = get_supabase()
        
        try:
            # Sign in with Supabase Auth
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # Get user info from our users table
            user_response = supabase.table('users').select('*').eq('email', email).execute()
            
            if user_response.data:
                user_data = user_response.data[0]
                user = User(
                    id=user_data['id'],
                    email=user_data['email'],
                    user_type=user_data['user_type'],
                    name=user_data.get('name')
                )
                
                login_user(user)
                
                # Redirect based on user type
                if user.user_type == 'buyer':
                    return redirect(url_for('main.buyer_dashboard'))
                else:
                    return redirect(url_for('main.seller_dashboard'))
            else:
                flash('User not found')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}')
        
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.login'))

@main.route('/buyer')
@login_required
def buyer_dashboard():
    if current_user.user_type != 'buyer':
        flash('Access denied. Buyer account required.')
        return redirect(url_for('main.login'))
    
    return render_template('buyer_dashboard.html', name=current_user.name or current_user.email)

@main.route('/seller')
@login_required
def seller_dashboard():
    if current_user.user_type != 'seller':
        flash('Access denied. Seller account required.')
        return redirect(url_for('main.login'))
    
    return render_template('seller_dashboard.html', name=current_user.name or current_user.email)