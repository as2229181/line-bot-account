from datetime import datetime
from typing import Callable, Dict

from flask import current_app
from linebot.models import MessageAction, QuickReply, QuickReplyButton, TextSendMessage

from consts.linebot_const import AccountAction, AccountStep
from middlewares.accounting import AccountingRecorder


class AccountExecUnit:
    # TODO: 抽出 handle 成 class BaseHandle
    def __init__(self, user_uuid, input_text, params=None, action=None):
        self._user_uuid = user_uuid
        self._input_text = input_text
        self._processed_text = self._extract_text()
        self._action = action
        self._params = params
        self._title = self._get_title()
        self._account_manager = getattr(current_app, 'account_manager', None)

    @staticmethod
    def _get_title():
        cur = datetime.now()
        cur_year, cur_month = cur.year, cur.month
        return f'{cur_year}-{cur_month:02d}'

    def _extract_text(self):
        return self._input_text.split()

    @staticmethod
    def _handle_initial():
        new_session = {'step': AccountStep.PAYER}
        reply = TextSendMessage(text='開始記帳流程，請輸入付款人姓名，如需取消請輸入「account-cancel」')
        return new_session, reply

    def _handle_payer(self, session):
        session.update(
            {
                'step': AccountStep.DEBTOR,
                'payer': self._processed_text[0],
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入欠款人姓名，如需取消請輸入「account-cancel」')
        return reply

    def _handle_debtor(self, session):
        session.update(
            {
                'step': AccountStep.AMOUNT,
                'debtor': self._processed_text[0],
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入金額，如需取消請輸入「account-cancel」')
        return reply

    def _handle_amount(self, session):
        if len(self._processed_text) != 1 or not self._processed_text[0].isdigit():
            reply = TextSendMessage(text='金額輸入錯誤，請重新輸入，如需取消請輸入「account-cancel」')
            return reply
        amount = int(self._processed_text[0])
        session.update(
            {
                'step': AccountStep.TYPE,
                'amount': amount,
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入分帳類型\n代墊請輸入 「advance」\n 均分請輸入 「split」 \n如需取消請輸入「account-cancel」')
        return reply

    def _handle_type(self, session):
        session.update(
            {
                'step': AccountStep.CATEGORY,
                'type': self._processed_text[0],
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入分類(目前只開放輸入一種)，如需取消請輸入「account-cancel」')
        return reply

    def _handle_category(self, session):
        category = None if not self._processed_text[0] else self._processed_text[0]
        session.update(
            {
                'step': AccountStep.DESCRIPTION,
                'category': category,
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入備註\n如需取消請輸入「account-cancel」')
        return reply

    def _handle_description(self, session):
        session.update(
            {
                'step': AccountStep.DATE,
                'description': self._input_text.strip(),
            }
        )
        reply = TextSendMessage(text='記帳流程進行中，請輸入帳款時間(格式範例:2025-05-28)\n如需取消請輸入「account-cancel」')
        return reply

    def _handle_date(self, session):
        date = self._input_text.split('-')
        year, month, day = date[0], date[1], date[2]
        session.update(
            {
                'step': AccountStep.FINISH,
                'date': f'{year}-{month}-{day}',
            }
        )
        reply = TextSendMessage(
            text=(
                f'記帳流程完成,確認資料是正確\n'
                f'付款人:{session.get("payer")}\n'
                f'欠款人:{session.get("debtor")}\n'
                f'金額:{session.get("amount")}\n'
                f'類型:{session.get("type")}\n'
                f'分類:{session.get("category")}\n'
                f'時間:{session.get("date")}\n'
            ),
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ 正確，送出', text='confirm')),
                    QuickReplyButton(action=MessageAction(label='❌ 重新輸入', text='restart')),
                ],
            ),
        )
        return reply

    def _handle_finish(self, session):
        status = self._processed_text[0]
        if status == 'restart':
            new_session, reply = self._handle_initial()
            self._account_manager.set_session(self._user_uuid, new_session)
            return reply

        if status == 'confirm':
            AccountingRecorder.record(
                payer_name=session.get('payer'),
                debtor_name=session.get('debtor'),
                amount=session.get('amount'),
                _type=session.get('type'),
                category=session.get('category'),
                description=session.get('description'),
                date=session.get('date'),
            )
            reply = TextSendMessage(text='記帳完成!')
            return reply

    def _cancel(self):
        self._account_manager.delete_session(user_uuid=self._user_uuid)
        reply = TextSendMessage(text='❌ 已取消記帳流程，如需重新記帳請輸入「account」')
        return reply

    def exec(self) -> TextSendMessage:
        # 檢查記帳流程是否進行中
        session = self._account_manager.get_session(self._user_uuid)

        # 無 session 建立新的記帳流程
        if not session:
            session, reply = self._handle_initial()
            self._account_manager.set_session(self._user_uuid, session)
            return reply

        # 取消記帳流程記帳流程
        if self._action == AccountAction.CANCEL:
            reply = self._cancel()
            return reply

        current_step = session.get('step')
        if current_step == AccountStep.FINISH:
            reply = self._handle_finish(session)
            # 完成記帳刪除 session
            self._account_manager.delete_session(self._user_uuid)
            return reply

        step_handler_map: Dict[str, Callable[[dict], TextSendMessage]] = {
            AccountStep.PAYER: self._handle_payer,
            AccountStep.DEBTOR: self._handle_debtor,
            AccountStep.AMOUNT: self._handle_amount,
            AccountStep.TYPE: self._handle_type,
            AccountStep.CATEGORY: self._handle_category,
            AccountStep.DESCRIPTION: self._handle_description,
            AccountStep.DATE: self._handle_date,
        }

        handler = step_handler_map.get(current_step)
        if handler:
            reply = handler(session)
        else:
            reply = TextSendMessage(text='❌ 無法辨識的流程階段，請輸入「account-cancel」重新開始。')
        self._account_manager.set_session(self._user_uuid, session)
        return reply
