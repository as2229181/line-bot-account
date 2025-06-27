from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from database import db


class ClearedSpilt(db.Model):
    __tablename__ = 'cleared_splits'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)

    from_whom_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("users.uuid"))
    to_whom_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("users.uuid"))

    created_datetime = db.Column(db.DateTime, default=datetime.now)
