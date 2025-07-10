from decimal import ROUND_HALF_UP, Decimal

from common.db_tool import DBTool
from common.debug_tool import DebugTool
from common.exception import ValidationError
from common.id_tool import IDTool
from consts.linebot_const import PaymentType
from repositories.payment_repository import PaymentRepository
from repositories.split_repository import SplitRepository
from repositories.user_repository import UserRepository


class AccountingRecorder:
    @staticmethod
    def _transfer_to_decimal(number):
        return Decimal(number).quantize(Decimal('0.00'), ROUND_HALF_UP)

    @classmethod
    def record(
        cls,
        payer_name,
        debtor_name,
        amount,
        _type,
        category,
        description,
        date,
    ):
        # TODO: 未來要支援複數付款者及欠款者
        payer = UserRepository.get_by_username(payer_name)
        debtor = UserRepository.get_by_username(debtor_name)

        if not payer or not debtor:
            msg = 'payer or debtor does not exist'
            DebugTool.debug(msg=msg)
            raise ValidationError()
        _type = PaymentType.key_to_value(_type)

        payment = PaymentRepository.create(
            uuid=IDTool.get_uuid(),
            payer_uuid=payer.uuid,
            amount=amount,
            _type=_type,
            category=category,
            description=description,
            date=date,
            do_commit=False,
        )

        if not payment:
            msg = 'payment create failed'
            DebugTool.debug(msg=msg)
            raise ValidationError()

        DBTool.flush()

        final_amount = amount if _type == PaymentType.ADVANCED else amount / 2
        decimal_final_amount = cls._transfer_to_decimal(str(final_amount))
        split = SplitRepository.create(
            uuid=IDTool.get_uuid(),
            payment_uuid=payment.uuid,
            debtor_uuid=debtor.uuid,
            amount=decimal_final_amount,
            do_commit=False,
        )
        if not split:
            msg = 'split create failed'
            DebugTool.debug(msg=msg)
            raise ValidationError()

        DBTool.commit()
        return
