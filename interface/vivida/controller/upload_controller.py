import json
import zipfile
from io import BytesIO

import requests
from flask import Blueprint, render_template, request, make_response, redirect
from pathlib import Path

from config import API_HOST
from util import converter

upload_page_controller = Blueprint("upload_page_controller", __name__, template_folder="../static")

@upload_page_controller.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        user_id = request.cookies.get('user_id')

        if not user_id:
            redirect_response = make_response(redirect("/auth"))
            return redirect_response


        # body = {
        #     "user_id": user_id,
        #
        #     "date": request.form.get("date"),
        #     "name": request.form.get("name"),
        #     "description": request.form.get("description")
        # }

        body = request.form.to_dict()

        body["user_id"] = user_id
        body["neurological_symptoms"] = list(map(str.strip ,body["neurological_symptoms"].split(",")))

        for key, value in body.items():
            print(key, value)

        headers = {"Content-Type": "application/json"}
        response = requests.post(API_HOST + "/vivida/api/patient/create", data=json.dumps(body), headers=headers)

        if response.status_code == 201:
            redirect_response = make_response(redirect("/dashboard"))
            return redirect_response
        else:
            return render_template("error_template.html", status_code=response.status_code, error=response.text)


    return render_template("upload_template.html")
