from flask import Flask
from config import Config
from models.user import db
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
import os
from flask import redirect, url_for


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def home():
    return redirect(url_for('auth.register'))


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialisation de la base de données
db.init_app(app)

# Enregistrement des blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)



# Creation des tables de la base de données 
with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)