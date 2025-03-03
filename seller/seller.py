from flask import Blueprint, render_template, current_app, jsonify, request
 
seller = Blueprint("seller", __name__, static_folder="static", template_folder="templates")
 
@seller.route("/", methods=["GET", "POST"])
@seller.route("/home", methods=["GET", "POST"])
def home():
    try:
        products = current_app.supabase.table('product').select('*').execute()
        
        if not products.data:
            print("Product not found in the database")
            return render_template("seller.html", products=None)
           
        print("Successfully fetched product")
        return render_template("seller.html", product=products.data)  # Pass single product
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
    
@seller.route("/update_product/<p_id>", methods=["GET", "POST"])
def update_product(p_id):
    if request.method == "POST":
        # Get the form data
        new_p_id = request.form.get("p_id")
        p_name = request.form.get("p_name")
        p_brand = request.form.get("p_brand")
        p_condition = request.form.get("p_condition")
        p_type = request.form.get("p_type")
        p_quality = request.form.get("p_quality")
        p_quantity = request.form.get("p_quantity")
        p_price = request.form.get("p_price")
        p_material = request.form.get("p_material")
        p_design = request.form.get("p_design")

        # Build a dictionary of fields to update. Only include those that have values.
        update_data = {}
        if new_p_id:
            update_data["p_id"] = new_p_id
        if p_name:
            update_data["p_name"] = p_name
        if p_brand:
            update_data["p_brand"] = p_brand
        if p_condition:
            update_data["p_condition"] = p_condition
        if p_type:
            update_data["p_type"] = p_type
        if p_quality:
            update_data["p_quality"] = p_quality
        if p_quantity:
            update_data["p_quantity"] = p_quantity
        if p_price:
            update_data["p_price"] = p_price
        if p_material:
            update_data["p_material"] = p_material
        if p_design:
            update_data["p_design"] = p_design

        # Ensure that at least one field is provided to update.
        if not update_data:
            return render_template("update_product.html", error="Please provide at least one field to update", product={})

        try:
            # Update the product in the 'product' table using p_id as the filter.
            result = current_app.supabase.table('product').update(update_data).eq('p_id', p_id).execute()
            if result.data:
                success_message = "Product updated successfully!"
                updated_product = result.data[0]
                return render_template("update_product.html", product=updated_product, success=success_message)
            else:
                return render_template("update_product.html", error="Failed to update product", product={})
        except Exception as e:
            print(f"Update error: {str(e)}")
            return render_template("update_product.html", error="An error occurred during product update", product={})

    # For GET requests, fetch the current product details
    try:
        result = current_app.supabase.table('product').select('*').eq('p_id', p_id).execute()
        if result.data:
            product = result.data[0]
        else:
            product = {}
    except Exception as e:
        print(f"Fetch error: {str(e)}")
        product = {}

    return render_template("update_product.html", product=product)