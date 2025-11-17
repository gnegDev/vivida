from flask import Blueprint, request, make_response, redirect, url_for, render_template
import requests
import json

from config import API_HOST

log_in_controller = Blueprint("log_in_controller", __name__, template_folder="../static")

@log_in_controller.route("/login", methods=["POST"])
def log_in_user():
    body = {
        "email": request.form.get("email"),
        "password": request.form.get("password")
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_HOST + "/vivida/api/auth/login", data=json.dumps(body), headers=headers)

    if response.status_code == 200:
        user_id = response.json()["id"]

        redirect_response = make_response(redirect("/dashboard"))
        redirect_response.set_cookie("user_id", user_id)

        return redirect_response

    return render_template("error_template.html", status_code=response.status_code, error=response.text, link="/auth")
