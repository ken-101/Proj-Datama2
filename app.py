from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
from supabase import create_client

from buyer.buyer import buyer 
from seller.seller import seller
from loginlogout.loginlogout import auth
from config.config import Config

app = Flask(__name__)

# Configure Flask app
app.config.from_object(Config)
app.secret_key = secrets.token_hex(32)

# Initialize Supabase client
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# Make Supabase client available to the app context
app.supabase = supabase

# Register blueprints
app.register_blueprint(buyer, url_prefix="/buyer")
app.register_blueprint(seller, url_prefix="/seller")
app.register_blueprint(auth, url_prefix="/auth")

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("home"))
    return render_template("landing.html")

@app.route("/home")
def home():
    if not session.get("user_id"):
        return render_template("landing.html")
    
    try:
        # Get user data from Supabase
        user = supabase.table('users').select('*').eq('user_id', session['user_id']).execute()
        if not user.data:
            session.clear()
            return redirect(url_for("auth.login"))
            
        user_role = user.data[0]['user_role']
        
        # Redirect based on role
        if user_role == 'buyer':
            return redirect(url_for('buyer.home'))
        elif user_role == 'seller':
            return redirect(url_for('seller.home'))
        else:
            return render_template("home.html", user=user.data[0])
            
    except Exception as e:
        print(f"Error: {str(e)}")
        session.clear()
        return render_template("landing.html")
@app.route("/db")
def db():
    try:
        # Fetch products from Supabase
        products = supabase.table('product').select('*').execute()
        return render_template("db.html", products=products.data)
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return render_template("db.html", products=[])
@app.route('/updateform')
def update_form():
    return render_template('update.html')
@app.route('/update', methods=['POST'])
def update_data():
    # Get data from the request
    data = request.get_json()

    # Extract the values to update
    table_name = data.get('table_name')
    record_id = data.get('id')  # assuming the record has an 'id' field
    new_data = data.get('new_data')  # New data to update

    # Check if the data is provided correctly
    if not table_name or not record_id or not new_data:
        return jsonify({"error": "Missing required fields"}), 400

    # Perform the update operation in Supabase
    try:
        # Update the record in the specified table by ID
        response = supabase.table(table_name).update(new_data).eq('id', record_id).execute()

        # Check the response for success
        if response.status_code == 200:
            return jsonify({"message": "Record updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update record", "details": response.json()}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
