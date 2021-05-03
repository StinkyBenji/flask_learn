import os
from flask import Flask, request, jsonify, redirect, send_file, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models.models import db, login_manager, User, TraceFiles
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import json
import requests
from werkzeug.utils import secure_filename


ALLOWED_EXTENSTIONS = {}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = '880b839137def421'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@postgres_server:5432/io_trace"
    app.config['SQLALCHEMY_TRACK_NOTIFICATIOIN'] = False
    app.config['UPLOAD_PATH'] = UPLOAD_PATH  # define a upload path

    db.init_app(app)
    migrate = Migrate(app, db)

    bcrypt = Bcrypt()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    @app.route('/home', methods=['GET'])
    def home():
        return "homepage"

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        user_data = request.form
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        newUser = User(username=username, email=email,
                       password=hashed_password)

        try:
            db.session.add(newUser)
            db.session.commit()
        except:
            failres = {
                "type": "warning",
                "info": "Registration failed!"
            }
            return jsonify(failres)

        res = {
            "type": "success",
            "info": "registered successfully"
        }
        return jsonify(res)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form = request.form
        user = User.query.filter_by(email=form['email']).first()
        if user and bcrypt.check_password_hash(user.password, form['password']):
            login_user(user)
            res = {
                "info": "User login succeed!",
                "next_page": "home",
                "type": "success"
            }
            return jsonify(res)
        else:
            failres = {
                "info": "user login failed",
                "type": "warning"
            }
            return jsonify(failres)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(request.url)

    @app.route("/upload", methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'POST':
            if 'file' not in request.files:
                res = {
                    "info": "no file!",
                    "type": "warning"
                }
                return jsonify(res)

            file = request.files['file']
            if file.filename == '':
                res = {
                    'info': 'no selected file',
                    'type': 'warning'
                }
                return jsonify(res)
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                res = {
                    'info': 'upload successfully',
                    'type': 'success'
                }
                return jsonify(res)
                # redirect(url_for('files'))
        return redirect(url_for('files'))

    @ app.route("/files", methods=['GET'])
    def list_files():
        files = []
        for filename in os.listdir(app.config['UPLOAD_PATH']):
            path = os.path.join(app.config['UPLOAD_PATH'], filename)
            if os.path.isfile(path):
                files.append(filename)
        return jsonify(files)

    @ app.route("/delete/<filename>", methods=['GET', 'POST'])
    @ login_required
    def delete(filename):
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        os.remove(file_path)
        return "delete files"

    @ app.route("/download/<filename>", methods=['GET'])
    def download(filename):
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        return send_from_directory(file_path)

    @ app.route("/analyze/<filename>", methods=['GET', 'POST'])
    def analyze(filename):
        # import the function
        return "analyze files"

    return app
