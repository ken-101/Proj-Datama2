from flask import Blueprint, render_template, current_app, session, request, redirect, url_for
from datetime import datetime
import uuid

buyer = Blueprint("buyer", __name__, static_folder="static", template_folder="templates")

@buyer.route("/index", methods=["GET", "POST"])
def index():
    return render_template("dashboard.html")

@buyer.route("/home", methods=["GET", "POST"])
def home():
    try:
        # Fetch all products from the product table
        products = current_app.supabase.table('product').select('*').execute()
        return render_template("buyer_dashboard.html", products=products.data)
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return render_template("buyer_dashboard.html", products=None)

@buyer.route("/history", methods=["GET", "POST"])
def history():
    try:
        transactions = current_app.supabase.table ('transaction').select('*').eq('c_id', session['user_id']).order('t_date', desc=True).execute()
        return render_template("history.html", transactions=transactions.data)
    except Exception as e:
        print(f"Error fetching transactions: {str(e)}")
        return render_template("history.html", transactions=None)

@buyer.route("/order_1/<int:product_id>", methods=["GET"])
def order_1(product_id):
    try:
        product = current_app.supabase.table('product').select('*').eq('p_id', product_id).execute().data[0]
        return render_template("order_1.html", product=product)
    except Exception as e:
        print(f"Error fetching product: {str(e)}")
        return redirect(url_for('buyer.home'))

@buyer.route("/process_order_1", methods=["POST"])
def process_order_1():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    
    try:
        product = current_app.supabase.table('product').select('*').eq('p_id', product_id).execute().data[0]
        
        # Check if requested quantity is available
        if quantity > product['p_quantity']:
            return redirect(url_for('buyer.order_1', product_id=product_id))
            
        # Update product quantity
        new_quantity = product['p_quantity'] - quantity
        current_app.supabase.table('product').update({'p_quantity': new_quantity}).eq('p_id', product_id).execute()
        
        total_amount = quantity * product['p_price']
        return render_template("order_2form.html", product=product, quantity=quantity, total_amount=total_amount)
    except Exception as e:
        print(f"Error processing order step 1: {str(e)}")
        return redirect(url_for('buyer.home'))

@buyer.route("/process_order_2", methods=["POST"])
def process_order_2():
    try:
        # Get form data
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        total_amount = float(request.form.get('total_amount'))
        shipping_address = f"{request.form.get('address')}, {request.form.get('city')}"
        
        # Create transaction record
        transaction_data = {
            'c_id': session['user_id'],
            't_type': request.form.get('payment_method'),
            't_shipping_address': shipping_address,
            't_date': datetime.now().isoformat(),
            't_amount': total_amount,
            't_status': 'Processing'
        }
        
        # Insert transaction
        transaction = current_app.supabase.table('transaction').insert(transaction_data).execute()
        
        # Update product quantity
        product = current_app.supabase.table('product').select('*').eq('p_id', product_id).execute().data[0]
        new_quantity = product['p_quantity'] - quantity
        current_app.supabase.table('product').update({'p_quantity': new_quantity}).eq('p_id', product_id).execute()
        
        # Get the invoice number from the inserted transaction
        invoice_number = transaction.data[0]['t_invoice']
        
        return render_template("order_3.html", invoice_number=invoice_number, total_amount=total_amount)
    except Exception as e:
        print(f"Error processing order step 2: {str(e)}")
        return redirect(url_for('buyer.home'))

@buyer.route("/update_user", methods=["GET", "POST"])
def update_user():
    try:
        if request.method == "POST":
            # Get form data
            name = request.form.get('c_name')
            password = request.form.get('c_password')
            address = request.form.get('c_address')
            city = request.form.get('c_city')
            contact = request.form.get('c_contact')
            gender = request.form.get('c_gender')
            status = request.form.get('c_status')
            role = request.form.get('c_role')
            
            # Update user data in the database
            user_data = {}
            if name:
                user_data['c_name'] = name 
            if password:
                user_data['c_password'] = password
            if address:
                user_data['c_address'] = address
            if city:
                user_data['c_city'] = city
            if contact:
                user_data['c_contact'] = contact
            if gender:
                user_data['c_gender'] = gender
            if status:
                user_data['c_status'] = status
            if role:
                user_data['c_role'] = role
            
            if user_data:
                current_app.supabase.table('customer').update(user_data).eq('c_id', session['user_id']).execute()
                return render_template("update_user.html", success="Profile updated successfully", user=user_data)
            else:
                return render_template("update_user.html", error="No data provided for update")
        
        # GET request - fetch current user data
        user = current_app.supabase.table('customer').select('*').eq('c_id', session['user_id']).execute().data[0]
        return render_template("update_user.html", user=user)
    
    except Exception as e:
        print(f"Error updating user profile: {str(e)}")
        return render_template("update_user.html", error="Failed to update profile")
