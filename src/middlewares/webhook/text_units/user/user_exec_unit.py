import re
from typing import Callable, Dict, Union

from flask import current_app
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    MessageAction,
    QuickReply,
    QuickReplyButton,
    TemplateSendMessage,
    TextSendMessage,
)

from common.id_tool import IDTool
from consts.linebot_const import CreateUserStep, UserAction
from middlewares.webhook.text_units.base_text_exec_unit import BaseTextExecUnit
from repositories.user_repository import UserRepository


class UserExecUnit(BaseTextExecUnit):
    _DEFAULT_LABEL = '進行指令'

    def __init__(self, user_uuid, input_text, params=None, action=None):
        super().__init__(user_uuid, input_text, params, action)
        self._user_manager = getattr(current_app, 'user_manager', None)
        self._process_text = self._processed_text()
        self._EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def _validate_email(self, email):
        return bool(self._EMAIL_PATTERN.fullmatch(email))

    def _processed_text(self):
        return self._input_text.split()

    @staticmethod
    def _start():
        new_session = {'step': CreateUserStep.USERNAME}
        reply = TextSendMessage(text='開始建立使用者流程!\n 請輸入使用者姓名！')
        return new_session, reply

    @classmethod
    def _get_carousel_column(cls, title, text, action, label=None):
        column = CarouselColumn(
            title=title,
            text=text,
            actions=[MessageAction(label=label or cls._DEFAULT_LABEL, text=f'user-{action}')],
        )

        return column

    def _show_user_actions(self):
        actions = UserAction.get_values()
        reply = TemplateSendMessage(
            alt_text='可用指令',
            template=CarouselTemplate(
                columns=[
                    self._get_carousel_column(
                        title='可用指令',
                        text=f'user-{action}',
                        action=action,
                    )
                    for action in actions
                ]
            ),
        )
        return reply

    def _cancel(self):
        self._user_manager.delete_create_session(self._user_uuid)
        reply = TextSendMessage(text='取消建立使用者流程！\n輸入 user 操作使用者相關資訊！')
        return reply

    def _set_username(self, session):
        username = self._input_text
        session.update(
            {
                'step': CreateUserStep.EMAIL,
                'username': username,
            }
        )
        reply = TemplateSendMessage(
            alt_text='創建使用者流程進行中請輸入 email\n 如需取消流程請按下取消按鈕',
            template=CarouselTemplate(
                columns=[
                    self._get_carousel_column(
                        title='創建使用者',
                        text='創建使用者流程進行中請輸入 email\n 如需取消流程請按下取消按鈕',
                        action=UserAction.CANCEL,
                        label='取消流程',
                    )
                ]
            ),
        )
        return reply

    def _set_email(self, session):
        email = self._input_text
        if not self._validate_email(email):
            reply = TemplateSendMessage(
                alt_text='email 格式錯誤\n 請重新輸入 email\n 如需取消流程請按下取消按鈕',
                template=CarouselTemplate(
                    columns=[
                        self._get_carousel_column(
                            title='創建使用者',
                            text='email 格式錯誤\n 請重新輸入 email\n 如需取消流程請按下取消按鈕',
                            action=UserAction.CANCEL,
                            label='取消流程',
                        )
                    ]
                ),
            )
            return reply
        session.update(
            {
                'step': CreateUserStep.DESCRIPTION,
                'email': email,
            }
        )
        reply = TemplateSendMessage(
            alt_text='創建使用者流程進行中請輸入 email\n 如需取消流程請按下取消按鈕',
            template=CarouselTemplate(
                columns=[
                    self._get_carousel_column(
                        title='創建使用者',
                        text='創建使用者流程進行中請輸入備註\n 如需取消流程請按下取消按鈕',
                        action=UserAction.CANCEL,
                        label='取消流程',
                    )
                ]
            ),
        )
        return reply

    def _set_description(self, session):
        description = self._input_text
        session.update(
            {
                'step': CreateUserStep.FINISH,
                'description': description,
            }
        )
        reply = TextSendMessage(
            text=f'請確認資料輸入是否正確\n'
            f'使用者名稱：{session.get("username")}\n'
            f'電子郵件：{session.get("email")}\n'
            f'描述：{session.get("description")}\n',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ 正確，送出', text='confirm')),
                    QuickReplyButton(action=MessageAction(label='❌ 重新輸入', text='restart')),
                ],
            ),
        )
        return reply

    def _finish(self, session):
        status = self._process_text[0]
        if status == 'restart':
            session, reply = self._start()
            self._user_manager.set_session(self._user_uuid, session)
            return reply
        if status == 'confirm':
            UserRepository.create(
                uuid=IDTool.get_uuid(),
                username=session.get('username'),
                email=session.get('email'),
                description=session.get('description'),
                do_commit=True,
            )
            reply = TextSendMessage(text='創建使用者完成!')
            return reply

    def exec(self) -> Union[TextSendMessage, TemplateSendMessage]:
        create_user_session = self._user_manager.get_create_session(self._user_uuid)
        if self._action is None and not create_user_session:
            reply = self._show_user_actions()
            return reply

        if self._action == UserAction.CREATE and not create_user_session:
            new_session, reply = self._start()
            self._user_manager.set_create_session(self._user_uuid, new_session)
            return reply

        if self._action == UserAction.CANCEL:
            reply = self._cancel()
            return reply

        current_step = create_user_session.get('step')

        if current_step == CreateUserStep.FINISH:
            reply = self._finish(create_user_session)
            self._user_manager.delete_create_session(self._user_uuid)
            return reply

        step_handle: Dict[
            str,
            Callable[
                [dict],
                Union[
                    TextSendMessage,
                    TemplateSendMessage,
                ],
            ],
        ] = {
            CreateUserStep.USERNAME: self._set_username,
            CreateUserStep.EMAIL: self._set_email,
            CreateUserStep.DESCRIPTION: self._set_description,
        }
        handle = step_handle.get(current_step)

        if handle:
            reply = handle(create_user_session)
            self._user_manager.set_create_session(self._user_uuid, create_user_session)
        else:
            reply = TextSendMessage(text='❌ 無法辨識的流程階段，請輸重新開始。', quick_reply=QuickReply())
        return reply
