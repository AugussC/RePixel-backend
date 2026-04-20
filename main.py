from flask import Flask
from flask_cors import CORS
from app.routes import user_routes
from app.routes.auth_routes import auth_routes
app.register_blueprint(user_routes)

app = Flask(__name__)
app.secret_key = "drmerygraciasportodalainfo"
CORS(app)  

app.register_blueprint(auth_routes, user_routes)

if __name__ == "__main__":
    app.run(debug=True)