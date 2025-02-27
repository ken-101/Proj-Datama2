from flask import Blueprint, render_template

buyer = Blueprint("buyer", __name__, static_folder="static", template_folder="templates")

@buyer.route("/", methods=["GET", "POST"])
def home():
    return render_template('buyer_dashboard.html')