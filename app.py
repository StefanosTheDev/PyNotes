from flask import Flask
from Database.db import db
from Controller.UserController import user_blueprint
from Controller.HomeController import home_blueprint
from Controller.NotesController import note_blueprint
from flask_navigation import Navigation
app = Flask(__name__, static_folder='static', template_folder='Templates')  # Set the static folder

import logging


# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress a warning message
app.secret_key = 'your_super_secret_key'  


logging.basicConfig(filename='LOG.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the database
db.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(note_blueprint)

@app.before_first_request

def create_tables():
    db.create_all()

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000)
