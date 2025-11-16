from base64 import b64encode

import requests
from flask import Blueprint, render_template

from config import API_HOST

scan_controller = Blueprint("scan_controller", __name__, template_folder="../static")
@scan_controller.route("/dashboard/<patient_id>", methods=["GET"])
def render_scan_page(patient_id):
    patient = requests.get(API_HOST + f"/vivida/api/patient/{patient_id}").json()

    patient_data = patient
    patient_data["patient_id"] = patient_id

    return render_template("scan_template.html", patient_data=patient_data)