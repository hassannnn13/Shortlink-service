from flask import Flask

def create_app(db_path="links.db"):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path

    from .views import bp as views_bp
    app.register_blueprint(views_bp)

    @app.route("/")
    def index():
        return ("shortlink service", 200)

    from .db import init_db
    init_db(app.config["DB_PATH"])

    return app
