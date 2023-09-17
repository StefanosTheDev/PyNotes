from Models.UserModel import UserModel
from flask import jsonify, session 
from Database.db import db
from GlobalExceptions.ServiceException import ServiceException
from sqlalchemy.exc import IntegrityError, OperationalError
import warnings
class UserService:
    def login(username, password):
        try:
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                return jsonify({"message": "User does not exist"}), 401
            elif user.password != password:
                return jsonify({"message": "Incorrect password"}), 401
        
        # Set user logged-in session
            session['logged_in'] = True
            session['user_id'] = user.id
            print(session)
            return jsonify({"message": user.json()})
        except Exception as e:
            return jsonify({"error": str(e)})

    def logout():
        session.clear()  # Clear all session data
        return jsonify({"message": "Logged out successfully!"})
    
    def create_user(username, password, role):
        try:
            validated_username = UserService.check_username(username)
            validated_pass = UserService.check_password(password)
            
            new_user = UserModel(username=validated_username, password=validated_pass, role=role)
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({'User Created': new_user.json()})
        except Exception as e:
            print(f"Could not add this user: {username} to the database", e)
            db.session.rollback()
            return jsonify({"error": "Unable to create user"}), 500
        
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
        try:
            if len(username) <= 5 or len(username) > 12:
                raise ValueError("Error with length of username") 
            has_upper = any(letter.isupper() for letter in username)
            has_lower = any(letter.islower() for letter in username)
            if not(has_upper and has_lower): 
                raise ValueError("Issue here with casing")
            return username
        except ValueError as e:
            print(e)
            raise

    def check_password(password):
        try:
            SPECIAL_CHARACTERS = "!@#$%^&*"
            if len(password) <= 5 or len(password) > 16:
                raise ValueError('Length Issue')
            has_upper = any(letter.isupper() for letter in password)
            has_lower = any(letter.islower() for letter in password)
            if not (has_upper and has_lower):
                raise ValueError("whoa no casing matches")
            if not any(char.isdigit() for char in password):
                raise ValueError("no numbers")
            if not any(char in SPECIAL_CHARACTERS for char in password):
                raise ValueError("no Character")
            return password
        except ValueError as e:
            print(e)
            raise 

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