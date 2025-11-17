from flask import Blueprint, make_response, redirect, render_template
import requests

from config import API_HOST

delete_controller = Blueprint("delete_controller", __name__, template_folder="../static")

@delete_controller.route("/dashboard/<scan_id>/delete", methods=["GET"])
def delete_scan(scan_id):
    response = requests.delete(API_HOST + f"/vivida/api/patient/delete/{scan_id}")

    if response.status_code == 204:
        redirect_response = make_response(redirect("/dashboard"))
        return redirect_response

    return render_template("error_template.html", status_code=response.status_code, error=response.text, link="/dashboard")
