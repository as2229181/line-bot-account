from database import db
from models.payment import Payment
from repositories.repo import Repo


class PaymentRepository(Repo):
    @staticmethod
    def create(
        uuid,
        payer_uuid,
        amount,
        _type,
        category,
        description,
        date,
        do_commit=True,
        do_flush=False,
    ):
        payment = Payment(
            uuid=uuid,
            payer_uuid=payer_uuid,
            amount=amount,
            type=_type,
            category=category,
            description=description,
            date=date,
        )
        db.session.add(payment)
        if do_commit:
            db.session.commit()
        if do_flush:
            db.session.flush(payment)
        return payment

    @staticmethod
    def get(uuid):
        payment = db.session.query(
            Payment,
        ).filter(
            uuid=uuid,
        )
        return payment

    @staticmethod
    def update(
        obj,
        payer_uuid=None,
        amount=None,
        category=None,
        description=None,
        date=None,
        do_commit=True,
        do_flush=False,
    ):
        if payer_uuid is not None:
            obj.payer_uuid = payer_uuid
        if amount is not None:
            obj.amount = amount
        if category is not None:
            obj.category = category
        if description is not None:
            obj.description = description
        if date is not None:
            obj.date = date

        if do_commit:
            db.session.commit()

        if do_flush:
            db.session.flush(obj)

        return obj

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        return
