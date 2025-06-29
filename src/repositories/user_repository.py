from database import db
from models.user import User
from repositories.repo import Repo


class UserRepository(Repo):
    @staticmethod
    def create(
        uuid,
        username,
        description,
        email,
        do_commit=True,
        do_flush=False,
    ):
        user = User(
            uuid=uuid,
            username=username,
            description=description,
            email=email,
        )
        db.session.add(user)
        if do_commit:
            db.session.commit()
        if do_flush:
            db.session.flush(user)
        return user

    @staticmethod
    def get(uuid):
        user = db.session.query(
            User,
        ).filter(
            uuid=uuid,
        )
        return user

    @staticmethod
    def update(
        obj,
        username=None,
        description=None,
        email=None,
        do_commit=True,
        do_flush=False,
    ):
        if username is not None:
            obj.username = username
        if description is not None:
            obj.description = description
        if email is not None:
            email.email = email

        if do_commit:
            db.session.commit()

        if do_flush:
            db.session.flush(obj)

        return obj

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        return
