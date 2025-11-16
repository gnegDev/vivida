import json

from flask import Blueprint, request, make_response, redirect, url_for, render_template
import requests

from config import API_HOST

sign_in_controller = Blueprint("sign_in_controller", __name__, template_folder="../static")

@sign_in_controller.route("/signin", methods=["POST"])
def sign_in_user():
    body = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "password": request.form.get("password")
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_HOST + "/vivida/api/auth/signin", data=json.dumps(body), headers=headers)

    if response.status_code == 201:
        user_id = response.json()["id"]

        redirect_response = make_response(redirect("/dashboard"))
        redirect_response.set_cookie("user_id", user_id)

        return redirect_response

    return render_template("error_template.html", status_code=response.status_code, error=response.text, link="/auth")
