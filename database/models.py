from datetime import datetime

from flask_login import UserMixin

from database.db import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    predictions = db.relationship(
        "Prediction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    area = db.Column(
        db.Float,
        nullable=False
    )

    bedrooms = db.Column(
        db.Integer,
        nullable=False
    )

    bathrooms = db.Column(
        db.Integer,
        nullable=False
    )

    floors = db.Column(
        db.Integer,
        default=1
    )

    parking = db.Column(
        db.Integer,
        default=0
    )

    furnishing = db.Column(
        db.String(50)
    )

    property_type = db.Column(
        db.String(50)
    )

    age = db.Column(
        db.Integer,
        default=0
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(500)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    area = db.Column(
        db.Float,
        nullable=False
    )

    bedrooms = db.Column(
        db.Integer,
        nullable=False
    )

    bathrooms = db.Column(
        db.Integer,
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    predicted_price = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )