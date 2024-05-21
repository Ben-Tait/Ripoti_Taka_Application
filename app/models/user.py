import flask
import hashlib
from datetime import datetime
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import login_manager
from app import db


@login_manager.user_loader
def load_user(user_id):
    """
    Queries the database for a record of currently logged in user
    Returns User object containing info about logged in user
    """
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class User(UserMixin, db.Model):
    __tablename__ = "user"
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(30))
    middleName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))

    userName = db.Column(db.String(50), unique=True, nullable=False)
    emailAddress = db.Column(db.String(100), nullable=False)
    passwordHash = db.Column(db.String(100), nullable=False)

    phoneNumber = db.Column(db.String(20))
    gender = db.Column(db.String(8), default="Female", nullable=False)
    locationAddress = db.Column(db.String(255), default="Nairobi West")

    about_me = db.Column(db.String(140))
    avatar_hash = db.Column(db.String(32))
    pointsAcquired = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    imageUrl = db.Column(db.String(200))
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    # relationships
    roleId = db.Column(db.Integer, db.ForeignKey("role.roleId"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.pointsAcquired is None:
            self.pointsAcquired = 5

        # Assign default role to user
        if self.role is None:
            from .role import Role

            if (
                self.emailAddress
                == flask.current_app.config["ADMINISTRATOR_EMAIL"]
            ):
                self.role = Role.query.filter_by(name="Administrator").first()

            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

        # Generate avatar hash
        if self.emailAddress is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def __repr__(self):
        return (
            f"<User(userId={self.userId}, userName='{self.userName}',"
            + f"emailAddress='{self.emailAddress}')>"
        )

    def get_id(self):
        return self.userId

    def gravatar_hash(self):
        return hashlib.md5(
            self.emailAddress.lower().encode("utf-8")
        ).hexdigest()

    def gravatar(self, size=100, default="identicon", rating="g"):
        url = "https://secure.gravatar.com/avatar"
        hash = self.avatar_hash or self.gravatar_hash()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)
