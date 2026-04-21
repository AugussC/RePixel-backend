from flask import Flask
from flask_cors import CORS


from app.routes.user_routes import user_routes
from app.routes.auth_routes import auth_routes
from app.routes.image_routes import image_routes
from scheduler import start_scheduler



app = Flask(__name__)
app.secret_key = "drmerygraciasportodalainfo"
CORS(app)  
start_scheduler()

app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(image_routes)

if __name__ == "__main__":
    app.run(debug=True)