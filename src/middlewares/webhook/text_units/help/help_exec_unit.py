from linebot.models import CarouselColumn, CarouselTemplate, MessageAction, TemplateSendMessage

from consts.linebot_const import TextJobType
from middlewares.webhook.text_units.base_text_exec_unit import BaseTextExecUnit


class HelpExecUnit(BaseTextExecUnit):
    def __init__(self, user_uuid, input_text, params=None, action=None):
        super().__init__(user_uuid, input_text, params, action)

    @staticmethod
    def _get_carousel_columns():
        values = TextJobType.get_values()
        columns = list()
        for index, value in enumerate(values):
            column = CarouselColumn(
                title=f'指令 {index + 1} 「{value}」',
                text=f'{value}',
                actions=[MessageAction(label='進行指令', text=f'{value}')],
            )
            columns.append(column)
        return columns

    def exec(self):
        reply = TemplateSendMessage(alt_text='可用指令', template=CarouselTemplate(columns=self._get_carousel_columns()))
        return reply
