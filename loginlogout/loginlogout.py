from flask import Blueprint, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

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
            user = current_app.supabase.table('customer').select('*').eq('c_email', email).execute()
            
            if not user.data:
                return render_template("login.html", error="Invalid email or password")
                
            user_data = user.data[0]
            
            # Verify password
            if user_data.get('c_password') != password:
                return render_template("login.html", error="Invalid email or password")

                
            # Set session data
            session['user_id'] = user_data['c_id']
            session['email'] = user_data['c_email']
            session['role'] = user_data['c_role']
            
            return redirect(url_for('home'))
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return render_template("login.html", error="An error occurred during login")
    
    return render_template("login.html")

@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("home"))  # Redirect to home page

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
            existing_user = current_app.supabase.table('customer').select('*').eq('c_email', email).execute()
            if existing_user.data:
                return render_template("signup.html", error="Email already registered")
        
            
            # Insert new user
            new_user = current_app.supabase.table('customer').insert({
                'c_email': email,
                'c_password': password,
                'c_role': role
            }).execute()
            
            if new_user.data:
                return redirect(url_for('auth.login'))
            else:
                return render_template("signup.html", error="Failed to create account")
                
        except Exception as e:
            print(f"Signup error: {str(e)}")
            return render_template("signup.html", error="An error occurred during signup")
            
    return render_template("signup.html")