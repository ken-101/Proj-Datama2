from flask import Flask, render_template, request, redirect, url_for, session
import secrets
from anotherapp import another 
app = Flask(__name__)
app.register_blueprint(another, url_prefix="")
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")  # Get role from form input
        if role in ["buyer", "seller", "admin"]:  # Ensure valid roles
            session["valid_role"] = role  # Mark session as valid
            return redirect(url_for("home", role=role))  # Redirect to /<role>
    else:
        if session.get("valid_role"):
            return redirect(url_for("home", role=session["valid_role"]))
    
        return render_template("login.html")  # Render form page

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("login"))  # Redirect to login page

@app.route("/<role>")
def home(role):
    if not session.get("valid_role"):  # If no valid session, redirect to login
        return redirect(url_for("login"))
    
    if role == "buyer":
        return render_template("buyer_dashboard.html") 
    elif role == "seller":
        return render_template("seller_dashboard.html") 
    elif role == "admin":
        return render_template("admin_dashboard.html")  # Fixed missing return
    else:
        return render_template("home.html")  # Default case

if __name__ == '__main__':
    app.run(debug=True)
