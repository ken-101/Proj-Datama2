from flask import Blueprint, render_template, current_app, jsonify
 
seller = Blueprint("seller", __name__, static_folder="static", template_folder="templates")
 
@seller.route("/", methods=["GET", "POST"])
@seller.route("/home", methods=["GET", "POST"])
def home():
    try:
        # Fetch only product with p_id = 1
        products = current_app.supabase.table('product').select('*').eq('p_id', 58).execute()
        
        if not products.data:
            print("Product not found in the database")
            return render_template("seller.html", products=None)
           
        print("Successfully fetched product")
        return render_template("seller.html", product=products.data[0])  # Pass single product
    except Exception as e:
        print(f"Error fetching product: {str(e)}")
        # Log the full error for debugging
        import traceback
        print(traceback.format_exc())
        return render_template("seller.html", product=None)

@seller.route("/delete_product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        # Convert product_id to integer first
        try:
            product_id = int(product_id)
        except ValueError:
            return jsonify({"message": "Invalid product ID format"}), 400

        # Verify if product exists before deleting
        product = current_app.supabase.table("product").select("*").eq("p_id", product_id).execute()
        print(f"Delete operation response: {product}")
        if not product.data:
            return jsonify({"message": "Product not found"}), 404

        # Delete the product from Supabase
        print(f"Before delete: product_id = {product_id}")
        result = current_app.supabase.table('product').delete().eq('p_id', product_id).execute()
        print(f"After delete: product_id = {product_id}")

        
        print(f"Delete operation response: {result}")  # Debugging log

        if result.data:
            return jsonify({
                "message": "Product deleted successfully",
                "deleted_id": product_id
            }), 200
        else:
            return jsonify({"message": "Failed to delete product"}), 500
            
    except Exception as e:
        print(f"Error deleting product: {str(e)}")
        return jsonify({
            "message": "Failed to delete product",
            "error": str(e)
        }), 500