from io import BytesIO

from flask import Blueprint, make_response, redirect, render_template, send_file
import requests

from config import API_HOST
from util.report_generator import generate_report

download_controller = Blueprint("download_controller", __name__, template_folder="../static")

@download_controller.route("/dashboard/<scan_id>/download", methods=["GET"])
def download_scan(scan_id):
    scan = requests.get(API_HOST + f"/scanity/api/scans/{scan_id}").json()
    scan_filename = scan["dicom_filename"]
    preview_filename = scan["filename"]

    scan_response = requests.get(API_HOST + f"/scanity/api/scans/file/{scan_filename}")
    preview_response = requests.get(API_HOST + f"/scanity/api/scans/file/{preview_filename}")

    if scan_response.status_code == 200 and preview_response.status_code == 200:
        report_bytes = generate_report(scan, scan_response.content, preview_response.content)
        # redirect_response = make_response(redirect(f"/dashboard/{scan_id}"))
        # return redirect_response
        file = BytesIO(report_bytes)
        return send_file(file, download_name="report.zip", mimetype="application/zip", as_attachment=True)

    return render_template("error_template.html", status_code=response.status_code, error=response.text, link=f"/dashboard/{scan_id}")
