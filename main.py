from flask import Flask
from flask_cors import CORS
from app.routes.user_routes import user_routes
from app.routes.auth_routes import auth_routes
from app.routes.image_routes import image_routes
from scheduler import iniciar_scheduler

app = Flask(__name__)
app.secret_key = "drmerygraciasportodalainfo"

CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
    "http://127.0.0.1:8080"
])


app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False, 
    SESSION_COOKIE_HTTPONLY=True
)

iniciar_scheduler()

app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(image_routes)

if __name__ == "__main__":
    app.run(debug=True)