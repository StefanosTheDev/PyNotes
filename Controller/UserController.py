from flask import request, render_template, jsonify, redirect, url_for, flash, Blueprint, session

from functools import wraps
from Services.UserService import UserService
from Forms.UserForms import RegisterForm
user_blueprint = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({"error": "Access denied: You're not logged in!"}), 403
        return f(*args, **kwargs)
    return decorated_function

@user_blueprint.route('/user/employees', methods=['GET'])
@login_required
def get_users():
     return UserService.display_users()

@user_blueprint.route('/user/update/<int:id>', methods=['PUT'])
def update_user(id):  # You need to include the 'id' parameter here.
    try:
        data = request.get_json()
        updatedUsername = data.get('username')
        updatedPass = data.get('password')
        updatedRole = data.get('role')

        if not all([updatedUsername, updatedPass, updatedRole]):
            return jsonify({"error": "All fields are required!"}), 400

        return UserService.update_user(id, updatedUsername, updatedPass, updatedRole)  # Pass all required parameters here.
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route('/user/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()

    try:
        if form.validate_on_submit():  # This will handle POST request and validation
            username = form.username.data
            password = form.password.data
            role = form.role.data

            # Assuming UserService.create_user() returns some meaningful response
            response = UserService.create_user(username, password, role)
            
            if response:
                flash("User created successfully!", "success")
                return redirect(url_for('login_user'))  # Redirect to a login page, for example

            flash("Error in registration. Try again.", "danger")
    except Exception as e:
        flash(str(e), "danger")
    
    return render_template('Home/register.html', form=form)


### Refractored 


@user_blueprint.route('/user/delete/<int:id>', methods=['DELETE'])
def admin_delete_employee_by_Id(id):
    return UserService.delete_user_by_Id(id)

@user_blueprint.route('/user/login', methods=['POST'])
def admin_login():
    try: 
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        return UserService.login(username, password)
    except Exception as error:
        return jsonify({"Login Error": str(error)}), 500
    
@user_blueprint.route('/user/logout', methods=['POST'])
def admin_logout():
    return UserService.logout()

