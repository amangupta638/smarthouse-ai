from functools import wraps

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from database.db import db
from database.models import (
    User,
    Property,
    Prediction
)


# ============================================================
# ADMIN BLUEPRINT
# ============================================================

admin_bp = Blueprint(
    "admin",
    __name__
)


# ============================================================
# ADMIN ACCESS DECORATOR
# ============================================================

def admin_required(function):

    @wraps(function)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != "admin":

            flash(
                "Access denied. Admin privileges required.",
                "danger"
            )

            return redirect(
                url_for("main.dashboard")
            )

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@admin_bp.route("/admin")
@admin_required
def admin_panel():

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    properties = Property.query.order_by(
        Property.created_at.desc()
    ).all()

    predictions = Prediction.query.order_by(
        Prediction.created_at.desc()
    ).all()

    return render_template(
        "admin.html",
        users=users,
        properties=properties,
        predictions=predictions
    )


# ============================================================
# ADD PROPERTY
# ============================================================

@admin_bp.route(
    "/admin/property/add",
    methods=["POST"]
)
@admin_required
def add_property():

    try:

        property_data = Property(

            title=request.form.get(
                "title",
                ""
            ).strip(),

            location=request.form.get(
                "location",
                ""
            ).strip(),

            area=float(
                request.form.get(
                    "area",
                    0
                )
            ),

            bedrooms=int(
                request.form.get(
                    "bedrooms",
                    0
                )
            ),

            bathrooms=int(
                request.form.get(
                    "bathrooms",
                    0
                )
            ),

            floors=int(
                request.form.get(
                    "floors",
                    1
                )
            ),

            parking=int(
                request.form.get(
                    "parking",
                    0
                )
            ),

            furnishing=request.form.get(
                "furnishing"
            ),

            property_type=request.form.get(
                "property_type"
            ),

            age=int(
                request.form.get(
                    "age",
                    0
                )
            ),

            price=float(
                request.form.get(
                    "price",
                    0
                )
            ),

            description=request.form.get(
                "description",
                ""
            ).strip(),

            image=request.form.get(
                "image",
                ""
            ).strip()
        )


        # Basic validation

        if not property_data.title:
            flash(
                "Property title is required.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        if not property_data.location:
            flash(
                "Location is required.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        if property_data.area <= 0:
            flash(
                "Area must be greater than zero.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        if property_data.bedrooms <= 0:
            flash(
                "Bedrooms must be greater than zero.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        if property_data.bathrooms <= 0:
            flash(
                "Bathrooms must be greater than zero.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        if property_data.price <= 0:
            flash(
                "Price must be greater than zero.",
                "danger"
            )
            return redirect(
                url_for("admin.admin_panel")
            )


        db.session.add(
            property_data
        )

        db.session.commit()


        flash(
            "Property added successfully.",
            "success"
        )


    except (ValueError, TypeError):

        db.session.rollback()

        flash(
            "Please enter valid property values.",
            "danger"
        )


    except Exception as exc:

        db.session.rollback()

        flash(
            f"Unable to add property: {exc}",
            "danger"
        )


    return redirect(
        url_for("admin.admin_panel")
    )


# ============================================================
# EDIT PROPERTY
# ============================================================

@admin_bp.route(
    "/admin/property/<int:property_id>/edit",
    methods=["POST"]
)
@admin_required
def edit_property(property_id):

    property_item = db.session.get(
        Property,
        property_id
    )


    if not property_item:

        flash(
            "Property not found.",
            "danger"
        )

        return redirect(
            url_for("admin.admin_panel")
        )


    try:

        property_item.title = request.form.get(
            "title",
            ""
        ).strip()

        property_item.location = request.form.get(
            "location",
            ""
        ).strip()

        property_item.area = float(
            request.form.get(
                "area",
                0
            )
        )

        property_item.bedrooms = int(
            request.form.get(
                "bedrooms",
                0
            )
        )

        property_item.bathrooms = int(
            request.form.get(
                "bathrooms",
                0
            )
        )

        property_item.floors = int(
            request.form.get(
                "floors",
                1
            )
        )

        property_item.parking = int(
            request.form.get(
                "parking",
                0
            )
        )

        property_item.furnishing = request.form.get(
            "furnishing"
        )

        property_item.property_type = request.form.get(
            "property_type"
        )

        property_item.age = int(
            request.form.get(
                "age",
                0
            )
        )

        property_item.price = float(
            request.form.get(
                "price",
                0
            )
        )

        property_item.description = request.form.get(
            "description",
            ""
        ).strip()

        property_item.image = request.form.get(
            "image",
            ""
        ).strip()


        if not property_item.title:
            raise ValueError(
                "Property title is required."
            )


        if not property_item.location:
            raise ValueError(
                "Location is required."
            )


        if property_item.area <= 0:
            raise ValueError(
                "Area must be greater than zero."
            )


        if property_item.bedrooms <= 0:
            raise ValueError(
                "Bedrooms must be greater than zero."
            )


        if property_item.bathrooms <= 0:
            raise ValueError(
                "Bathrooms must be greater than zero."
            )


        if property_item.price <= 0:
            raise ValueError(
                "Price must be greater than zero."
            )


        db.session.commit()


        flash(
            "Property updated successfully.",
            "success"
        )


    except (ValueError, TypeError) as exc:

        db.session.rollback()

        flash(
            str(exc),
            "danger"
        )


    except Exception as exc:

        db.session.rollback()

        flash(
            f"Unable to update property: {exc}",
            "danger"
        )


    return redirect(
        url_for("admin.admin_panel")
    )


# ============================================================
# DELETE PROPERTY
# ============================================================

@admin_bp.route(
    "/admin/property/<int:property_id>/delete",
    methods=["POST"]
)
@admin_required
def delete_property(property_id):

    property_item = db.session.get(
        Property,
        property_id
    )


    if not property_item:

        flash(
            "Property not found.",
            "danger"
        )

        return redirect(
            url_for("admin.admin_panel")
        )


    try:

        db.session.delete(
            property_item
        )

        db.session.commit()


        flash(
            "Property deleted successfully.",
            "success"
        )


    except Exception as exc:

        db.session.rollback()

        flash(
            f"Unable to delete property: {exc}",
            "danger"
        )


    return redirect(
        url_for("admin.admin_panel")
    )