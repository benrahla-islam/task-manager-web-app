from flask import Flask 
from flask_migrate import Migrate

from models.models import db 
from routes.auth import auth_bp , login_manager
from routes.other import other_bp

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)

login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(other_bp)

migrate = Migrate(app = app , db = db)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
