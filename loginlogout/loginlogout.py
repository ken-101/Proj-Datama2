from flask import Blueprint, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            return render_template("login.html", error="Please provide both email and password")
            
        try:
            # Query user from Supabase
            user = current_app.supabase.table('users').select('*').eq('user_email', email).execute()
            
            if not user.data:
                return render_template("login.html", error="Invalid email or password")
                
            user_data = user.data[0]
            
            # Verify password
            stored_password = user_data.get('user_password')
            if not stored_password or not check_password_hash(stored_password, password):
                return render_template("login.html", error="Invalid email or password")
                
            # Set session data
            session['user_id'] = user_data['user_id']
            session['email'] = user_data['user_email']
            session['role'] = user_data['user_role']
            
            return redirect(url_for('home'))
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return render_template("login.html", error="An error occurred during login")
    
    return render_template("login.html")

@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("login.login"))  # Redirect to login page using correct blueprint endpoint

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "buyer")
        
        if not email or not password:
            return render_template("signup.html", error="Please provide both email and password")
            
        try:
            # Check if user already exists
            existing_user = current_app.supabase.table('users').select('*').eq('user_email', email).execute()
            if existing_user.data:
                return render_template("signup.html", error="Email already registered")
                
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Insert new user
            new_user = current_app.supabase.table('users').insert({
                'user_email': email,
                'user_password': hashed_password,
                'user_role': role
            }).execute()
            
            if new_user.data:
                return redirect(url_for('login.login'))
            else:
                return render_template("signup.html", error="Failed to create account")
                
        except Exception as e:
            print(f"Signup error: {str(e)}")
            return render_template("signup.html", error="An error occurred during signup")
            
    return render_template("signup.html")