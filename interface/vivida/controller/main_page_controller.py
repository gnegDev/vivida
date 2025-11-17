from flask import Blueprint, render_template

main_page_controller = Blueprint("main_page_controller", __name__, template_folder="../static")

@main_page_controller.route("/", methods=["GET"])
def render_main_page():
    return render_template("main_template.html")