from base64 import b64encode

import requests
from flask import Blueprint, render_template, request, make_response, redirect

from config import API_HOST

dashboard_controller = Blueprint("dashboard_controller", __name__, template_folder="../static")
@dashboard_controller.route("/dashboard", methods=["GET"])
def render_main_page():
    user_id = request.cookies.get('user_id')

    if not user_id:
        redirect_response = make_response(redirect("/auth"))
        return redirect_response

    user = requests.get(API_HOST + f"/vivida/api/users/{user_id}")

    patients = list()

    for patient in user.json()["patient_clinical_profiles"]:
        patients.append({
            "patient_id":  patient["id"],
            "chemo_regimen": patient["patient_chemo_regimen"]
        })

    return render_template("dashboard_template.html", patients=patients)