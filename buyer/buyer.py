from flask import Blueprint, render_template, current_app

buyer = Blueprint("buyer", __name__, static_folder="static", template_folder="templates")

@buyer.route("/", methods=["GET", "POST"])
def home():
    try:
        # Fetch products from Supabase
        product = current_app.supabase.table('product').select('*').execute()
        
        if products.data:
            return render_template('buyer_dashboard.html', products=product.data)
        else:
            return render_template('buyer_dashboard.html', products=[], message="No products available")
            
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return render_template('buyer_dashboard.html', products=[], error="Failed to load products")