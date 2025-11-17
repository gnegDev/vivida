from flask import Flask
from jinja2 import Environment, FileSystemLoader

from controller.main_page_controller import main_page_controller

from controller.auth_page_controller import auth_page_controller
from controller.log_in_controller import log_in_controller
from controller.sign_in_controller import sign_in_controller

from controller.dashboard_controller import dashboard_controller
from controller.scan_controller import scan_controller
from controller.delete_controller import delete_controller
from controller.download_controller import download_controller

from controller.upload_controller import upload_page_controller

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('static'))

app.register_blueprint(main_page_controller)

app.register_blueprint(auth_page_controller)
app.register_blueprint(log_in_controller)
app.register_blueprint(sign_in_controller)

app.register_blueprint(dashboard_controller)
app.register_blueprint(scan_controller)
app.register_blueprint(delete_controller)
app.register_blueprint(download_controller)

app.register_blueprint(upload_page_controller)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=5000)
