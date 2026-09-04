from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import db
from database.models import User


# ============================================================
# AUTH BLUEPRINT
# ============================================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            return redirect(
                url_for("main.dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        name = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not name:

            flash(
                "Name is required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        if not email:

            flash(
                "Email is required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        if not password:

            flash(
                "Password is required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "This email is already registered.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )


        hashed_password = generate_password_hash(
            password
        )


        new_user = User(

            name=name,

            email=email,

            password_hash=hashed_password,

            role="user"
        )


        try:

            db.session.add(
                new_user
            )

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Registration failed. Please try again.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "register.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("index")
    )