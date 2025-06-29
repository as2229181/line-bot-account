from database import db
from models.split import Split
from repositories.repo import Repo


class SplitRepository(Repo):
    @staticmethod
    def create(
        uuid,
        payment_uuid,
        debtor_uuid,
        amount,
        do_commit=True,
        do_flush=False,
    ):
        split = Split(
            uuid=uuid,
            payment_uuid=payment_uuid,
            debtor_uuid=debtor_uuid,
            amount=amount,
        )
        db.session.add(split)
        if do_commit:
            db.session.commit()
        if do_flush:
            db.session.flush(split)
        return split

    @staticmethod
    def get(uuid):
        split = db.session.query(
            Split,
        ).filter(
            uuid=uuid,
        )
        return split

    @staticmethod
    def update(
        obj,
        payment_uuid=None,
        debtor_uuid=None,
        amount=None,
        deleted_datetime=None,
        do_commit=True,
        do_flush=False,
    ):
        if payment_uuid is not None:
            obj.payment_uuid = payment_uuid
        if debtor_uuid is not None:
            obj.debtor_uuid = debtor_uuid
        if amount is not None:
            obj.amount = amount
        if deleted_datetime is not None:
            obj.deleted_datetime = deleted_datetime

        if do_commit:
            db.session.commit()

        if do_flush:
            db.session.flush(obj)

        return obj
