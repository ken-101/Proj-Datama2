from flask import Blueprint, render_template

seller = Blueprint("seller", __name__, static_folder="static", template_folder="templates")

@seller.route("/", methods=["GET", "POST"])
def home():
    return render_template('seller_dashboard.html')