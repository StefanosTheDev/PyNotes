from flask import Blueprint, request, jsonify, session, render_template

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/', methods=['GET'])
def home_page():
    return render_template('Home/index.html')

@home_blueprint.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')

@home_blueprint.route('/contact', methods=['GET'])
def contact_page():
    return render_template('contact.html')

