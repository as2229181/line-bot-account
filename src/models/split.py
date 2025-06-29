from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from database import db


class Split(db.Model):
    __tablename__ = 'splits'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    payment_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("payments.uuid"))
    debtor_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("users.uuid"))

    amount = db.Column(db.Integer, nullable=False)

    deleted_datetime = db.Column(db.DateTime)
    updated_datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_datetime = db.Column(db.DateTime, default=datetime.now)
