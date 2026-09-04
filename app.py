import os
import joblib
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)

from flask_login import LoginManager

from database.db import db
from database.models import User, Property

from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "smart-house-ai-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///smarthouse.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ============================================================
# DATABASE
# ============================================================

db.init_app(app)


# ============================================================
# LOGIN MANAGER
# ============================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

MODEL_PATH = "models/linear_regression_model.pkl"

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "ML model not found. "
        "Please run: python ml/train.py"
    )


model = joblib.load(MODEL_PATH)

print("ML model loaded successfully.")


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH CHECK API
# ============================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "success": True,

        "message": "SmartHouse AI API is running",

        "model": "Linear Regression"

    })


# ============================================================
# PREDICTION API
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def api_predict():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "error": "Request body is required."

            }), 400


        required_fields = [

            "area",
            "bedrooms",
            "bathrooms",
            "floors",
            "location",
            "parking",
            "furnishing",
            "property_type",
            "age"

        ]


        missing = [

            field

            for field in required_fields

            if field not in data

        ]


        if missing:

            return jsonify({

                "success": False,

                "error": "Missing required fields",

                "missing": missing

            }), 400


        input_df = pd.DataFrame([{

            "area": float(
                data["area"]
            ),

            "bedrooms": int(
                data["bedrooms"]
            ),

            "bathrooms": int(
                data["bathrooms"]
            ),

            "floors": int(
                data["floors"]
            ),

            "location": data[
                "location"
            ],

            "parking": int(
                data["parking"]
            ),

            "furnishing": data[
                "furnishing"
            ],

            "property_type": data[
                "property_type"
            ],

            "age": int(
                data["age"]
            )

        }])


        prediction = float(
            model.predict(
                input_df
            )[0]
        )


        return jsonify({

            "success": True,

            "predicted_price": round(
                prediction,
                2
            ),

            "currency": "INR",

            "model": "Linear Regression"

        })


    except ValueError:

        return jsonify({

            "success": False,

            "error": "Invalid numeric input."

        }), 400


    except Exception as exc:

        return jsonify({

            "success": False,

            "error": str(exc)

        }), 500


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    with app.app_context():

        db.create_all()


        if not Property.query.first():

            properties = [

                Property(

                    title="Luxury Apartment",

                    location="Delhi",

                    area=1500,

                    bedrooms=3,

                    bathrooms=2,

                    floors=1,

                    parking=1,

                    furnishing="Furnished",

                    property_type="Apartment",

                    age=2,

                    price=8500000,

                    description=(
                        "Modern luxury apartment in Delhi."
                    )

                ),

                Property(

                    title="Modern Villa",

                    location="Lucknow",

                    area=2500,

                    bedrooms=4,

                    bathrooms=3,

                    floors=2,

                    parking=2,

                    furnishing="Furnished",

                    property_type="Villa",

                    age=3,

                    price=12000000,

                    description=(
                        "Spacious modern villa in Lucknow."
                    )

                ),

                Property(

                    title="Family House",

                    location="Noida",

                    area=1800,

                    bedrooms=3,

                    bathrooms=2,

                    floors=2,

                    parking=1,

                    furnishing="Semi-Furnished",

                    property_type="House",

                    age=5,

                    price=7500000,

                    description=(
                        "Comfortable family house."
                    )

                ),

                Property(

                    title="Premium Apartment",

                    location="Mumbai",

                    area=1200,

                    bedrooms=2,

                    bathrooms=2,

                    floors=1,

                    parking=1,

                    furnishing="Furnished",

                    property_type="Apartment",

                    age=4,

                    price=10000000,

                    description=(
                        "Premium apartment in Mumbai."
                    )

                )

            ]


            db.session.add_all(
                properties
            )

            db.session.commit()

            print(
                "Sample properties added successfully."
            )


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    return (
        "<h1>500 - Internal Server Error</h1>"
        "<p>Please check the Flask terminal for details.</p>"
    ), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print()
    print("=" * 60)
    print("SMART HOUSE AI")
    print("=" * 60)
    print(
        "Server: http://127.0.0.1:5000"
    )
    print(
        "Health API: http://127.0.0.1:5000/api/health"
    )
    print("=" * 60)
    print()

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )