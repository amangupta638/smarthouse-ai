import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from database.db import db
from database.models import (
    Prediction,
    Property
)

from nlp.query_parser import (
    parse_natural_query
)


# ============================================================
# MAIN BLUEPRINT
# ============================================================

main_bp = Blueprint(
    "main",
    __name__
)


# ============================================================
# DASHBOARD
# ============================================================

@main_bp.route("/dashboard")
@login_required
def dashboard():

    history = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        history=history
    )


# ============================================================
# HOUSE PRICE PREDICTION
# ============================================================

@main_bp.route(
    "/predict",
    methods=["GET", "POST"]
)
@login_required
def predict():

    if request.method == "POST":

        try:

            data = {

                "area": float(
                    request.form["area"]
                ),

                "bedrooms": int(
                    request.form["bedrooms"]
                ),

                "bathrooms": int(
                    request.form["bathrooms"]
                ),

                "floors": int(
                    request.form["floors"]
                ),

                "location": request.form[
                    "location"
                ],

                "parking": int(
                    request.form["parking"]
                ),

                "furnishing": request.form[
                    "furnishing"
                ],

                "property_type": request.form[
                    "prop_type"
                ],

                "age": int(
                    request.form["age"]
                )
            }


            # Import model here to avoid circular import
            from app import model


            # Convert input to DataFrame
            input_df = pd.DataFrame(
                [data]
            )


            # Generate prediction
            prediction = float(
                model.predict(
                    input_df
                )[0]
            )


            # Save prediction history
            new_prediction = Prediction(

                user_id=current_user.id,

                area=data["area"],

                bedrooms=data["bedrooms"],

                bathrooms=data["bathrooms"],

                location=data["location"],

                predicted_price=prediction

            )


            db.session.add(
                new_prediction
            )

            db.session.commit()


            # Find recommendations
            recommendations = Property.query.filter(

                Property.location
                == data["location"],

                Property.price
                <= prediction * 1.20

            ).limit(3).all()


            return render_template(

                "result.html",

                price=round(
                    prediction,
                    2
                ),

                recs=recommendations

            )


        except ValueError:

            db.session.rollback()

            flash(
                "Please enter valid numeric values.",
                "danger"
            )

            return redirect(
                url_for("main.predict")
            )


        except Exception as exc:

            db.session.rollback()

            flash(
                f"Prediction error: {exc}",
                "danger"
            )

            return redirect(
                url_for("main.predict")
            )


    return render_template(
        "predict.html"
    )


# ============================================================
# SMART NLP PROPERTY SEARCH
# ============================================================

@main_bp.route(
    "/smart-search",
    methods=["POST"]
)
def smart_search():

    query = request.form.get(
        "query",
        ""
    ).strip()


    if not query:

        return render_template(

            "properties.html",

            properties=[],

            query=""

        )


    parsed = parse_natural_query(
        query
    )


    results = Property.query


    # Location
    if parsed.get("location"):

        results = results.filter(

            Property.location
            == parsed["location"]

        )


    # Bedrooms
    if parsed.get("bedrooms"):

        results = results.filter(

            Property.bedrooms
            == parsed["bedrooms"]

        )


    # Budget
    if parsed.get("budget"):

        results = results.filter(

            Property.price
            <= parsed["budget"]

        )


    # Property type
    if parsed.get("property_type"):

        results = results.filter(

            Property.property_type
            == parsed["property_type"]

        )


    # Furnishing
    if parsed.get("furnishing"):

        results = results.filter(

            Property.furnishing
            == parsed["furnishing"]

        )


    final_results = results.all()


    return render_template(

        "properties.html",

        properties=final_results,

        query=query

    )


# ============================================================
# PROFILE
# ============================================================

@main_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

@main_bp.route("/history")
@login_required
def history():

    prediction_history = Prediction.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Prediction.created_at.desc()

    ).all()


    return render_template(

        "history.html",

        history=prediction_history

    )