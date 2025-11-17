from flask import Blueprint, render_template

auth_page_controller = Blueprint("auth_page_controller", __name__, template_folder="../static")

@auth_page_controller.route("/auth", methods=["GET"])
def render_auth_page():
    return render_template("auth_template.html")