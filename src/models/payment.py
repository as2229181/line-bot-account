from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from consts.linebot_const import PaymentType
from database import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    payer_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("users.uuid"))

    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False, default=PaymentType.SPLIT)

    category = db.Column(db.String(80))
    description = db.Column(db.Text)

    updated_datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_datetime = db.Column(db.DateTime, default=datetime.now)
