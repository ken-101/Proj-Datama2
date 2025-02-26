from flask import Blueprint, render_template

another = Blueprint("another", __name__, static_folder="static", template_folder="templates")

@another.route("/")
@another.route("/home")
def home():
    return render_template("login.html")