from flask import request, render_template, jsonify, redirect, url_for, flash, Blueprint, session

from functools import wraps
from Services.UserService import UserService
from Forms.UserForms import RegisterForm, LoginForm
from GlobalExceptions.ServiceException import ServiceException, UsernameError, PasswordError
user_blueprint = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({"error": "Access denied: You're not logged in!"}), 403
        return f(*args, **kwargs)
    return decorated_function

@user_blueprint.route('/user/employees', methods=['GET'])
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
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            role = form.role.data
            
            createdUser = UserService.create_user(username, password, role)
            if createdUser:
                flash("User created successfully!", "success")
                return redirect(url_for('user.admin_login'))
        
    except (UsernameError, PasswordError):  # You can catch multiple exceptions in a tuple
        flash("Ensure you meet the username and password requirements.", "danger")
        return render_template('Home/register.html', form=form)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  
        flash("An unexpected error occurred. Please try again later.", "danger")
        return render_template('Home/register.html', form=form)
    print('Hello World')
    return render_template('Home/register.html', form=form)

@user_blueprint.route('/user/delete/<int:id>', methods=['DELETE'])
def admin_delete_employee_by_Id(id):
    return UserService.delete_user_by_Id(id)

@user_blueprint.route('/user/login', methods=['GET', 'POST'])
def admin_login():

    form = LoginForm()
    try:
        if form.validate_on_submit():  # This will handle POST request and validation
            username = form.username.data
            password = form.password.data

            # Assuming UserService.create_user() returns some meaningful response
            response = UserService.login(username, password)
            
            if response:
                flash("User created successfully!", "success")
                return redirect(url_for('notes.get_notes'))  # Redirect to a login page, for example
            
    except (UsernameError, PasswordError):
        flash("Login Failed, Username and Password do not exist", 'danger')
        return render_template('Home/Login.html', form=form)
    
    return render_template('Home/Login.html', form=form)
    
@user_blueprint.route('/user/logout', methods=['POST'])
def admin_logout():
    return UserService.logout()

