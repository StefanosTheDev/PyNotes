import logging
from Models.UserModel import UserModel
from flask import jsonify, session 
from Database.db import db
from GlobalExceptions.ServiceException import UsernameError, PasswordError, ServiceException
from sqlalchemy.exc import IntegrityError, OperationalError
import warnings

class UserService:

    ## Steps for the login.
    ## Check for the username and if that exists, grab that object. If the password is equal to the password in the actual object. Return True
    ## If the username exits but password wrong though.
    def login(username, password):
        try:
            user = UserModel.query.filter_by(username=username).first() # query for the user oject.
            if not user:
                raise UsernameError("User does not exist")
            elif user.password == password:
                print(f"There is a match between {user.password} and {password}")
            elif user.password != password:
                raise PasswordError( "Incorrect password")
        
        # Set user logged-in session
            session['logged_in'] = True
            session['user_id'] = user.id
            return True
        except (UsernameError, PasswordError) as e:
            logging.error(e)
            raise

    def logout():
        session.clear()  # Clear all session data
        return jsonify({"message": "Logged out successfully!"})
    
    def create_user(username, password, role):  # assuming this is within a class
        try:
            UserService.check_username(username)
        # Assuming there's a similar method for password:
            UserService.check_password(password)
        
            new_user = UserModel(username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
        
            return True
        except (UsernameError, PasswordError) as e:
            logging.error(e)
            db.session.rollback()
            raise
        except Exception as e:
            logging.error(f"Could not add user: {username} to the database due to {str(e)}")
            db.session.rollback()
            raise
      
    def update_user(id, updatedUsername, updatedPass, updatedEmail, updatedRole):
        try:
        # Fetch the user by ID
            user = UserService.return_employee_by_Id(id)
        # Check and update username if changed
            if updatedUsername and updatedUsername != user.username:
                validated_username = UserService.check_username(updatedUsername)
                user.username = validated_username
        
        # Check and update password if changed
            if updatedPass:
                validated_pass = UserService.check_password(updatedPass)
                user.password = validated_pass  # ideally, you should hash the password before storing it
        
        # Check and update email if changed
            if updatedEmail and updatedEmail != user.email:
                validated_email = UserService.check_email_exist(updatedEmail)
                user.email = validated_email
        
        # Update role if changed
            if updatedRole:
                user.role = updatedRole  # assuming you have role field in your model and don't need to validate
        
        # Commit the changes
            db.session.commit()

            return jsonify({"Message": f"User with the {id} has been updated"})

        except ServiceException as e:  # catch the custom exception
            db.session.rollback()
            return jsonify({'Error': str(e)}), 500
        except Exception as e:  # catch all other exceptions
            db.session.rollback()
            return jsonify({f"Unexpected Error: {e}"})

    def display_users():
        try: 
            all_users = UserModel.query.all()
            if not all_users:
                raise Exception("No users were found in the database")
            users_json = [user.json() for user in all_users]
            return jsonify({'message': users_json})
        except Exception as error:
            print(error)
            return jsonify({'error': str(error)}), 400

    def delete_user_by_Id(id):
        try:
            user = UserService.return_employee_by_Id(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"message": f"User with ID {user.id} has been deleted from the database"}), 200
        except ServiceException as e:  # catch the custom exception
            db.session.rollback()
            return jsonify({'Error': str(e)}), 500
        except Exception as e:  # catch all other exceptions
            db.session.rollback()
            return jsonify({'Error': str(e)}), 500

    def return_employee_by_Id(id):     
        try:
            user = UserModel.query.get(id)
            if not user:
                raise ServiceException(f"No user found with the id {id}")
            return user
        except IntegrityError as e:
            raise ServiceException(f"Error Message: {e}")
        except OperationalError as e:  # catch any SQLAlchemy related errors
            raise ServiceException(f"Database Error: {e}")

    def removeAllSpaces(value):
        filteredVariable = "".join(value.split())
        return filteredVariable
    
    def check_username(username):
        if len(username) <= 5 or len(username) > 12:
            raise UsernameError("Error with length of username") 

        has_upper = any(letter.isupper() for letter in username)
        has_lower = any(letter.islower() for letter in username)
        if not(has_upper and has_lower):
            raise UsernameError("Username does not have an upper and lower case letter")
        return True
      

    def check_password(password):
        SPECIAL_CHARACTERS = "!@#$%^&*"
        if len(password) <= 5 or len(password) > 16:
            raise PasswordError('Password does not meet length requirements')

        has_upper = any(letter.isupper() for letter in password)
        has_lower = any(letter.islower() for letter in password)
        if not (has_upper and has_lower):
            raise PasswordError("Password does not meet capitalization requirements")
        if not any(char.isdigit() for char in password):
            raise PasswordError("Password does not contain a numeric value")
        if not any(char in SPECIAL_CHARACTERS for char in password):
            raise PasswordError("Password does not contain a special character")
    
        return True

    def Id_Req_Validation(request_id):
        if not request_id:
            raise ValueError('Request Id is null')
        parsedId = UserService.removeAllSpaces(request_id)
        try:
            return int(parsedId)
        except ValueError:
            error_msg = "Invalid ID format. Please enter a numeric ID."
            print(error_msg)
            raise ValueError(error_msg)
    def Hello_World(test):
        print("Hello World")