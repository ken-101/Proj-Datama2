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
@app.route('/update_product', methods=['POST'])
def update_product():
    data = request.get_json()

    # Extract the values from the request
    p_id = data.get('p_id')
    field = data.get('field')
    new_value = data.get('new_value')

    # Validate the input data
    if not p_id or not field or not new_value:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a dictionary to map the field names to the correct column names
    field_map = {
        'p_price': 'p_price',  # Corrected field name
        'p_name': 'name',
        'p_brand': 'brand',
        'p_condition': 'condition',
        'p_type': 'type',
        'p_quality': 'quality',
        'p_quantity': 'quantity',
        'p_material': 'material',
        'p_design': 'design'
    }

    # Check if the field is valid
    if field not in field_map:
        return jsonify({"error": "Invalid field selected"}), 400

    # Perform the update in the Supabase table
    try:
        # Update the record in the Supabase table by ID
        response = supabase.table('product').update({field_map[field]: new_value}).eq('p_id', p_id).execute()

        # Check for errors directly in `response.error`
        if response.error:  # This checks for the error attribute
            return jsonify({"error": response.error.message}), 500
        
        # If the update is successful, return a success message
        return jsonify({"message": "Product updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True)
