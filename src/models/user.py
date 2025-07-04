from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)

    is_active = db.Column(db.Bool, nullable=False, set_default=1)

    updated_datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_datetime = db.Column(db.DateTime, default=datetime.now)
