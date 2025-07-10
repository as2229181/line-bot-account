from database import db


class DBTool:
    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def expunge(obj):
        db.session.expunge(obj)

    @staticmethod
    def flush():
        db.session.flush()

    @staticmethod
    def roll_back():
        db.session.rollback()
