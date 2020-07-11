
from view import quick_reply, flex_message
from config import line_bot_api
from linebot.models import TextSendMessage, FlexSendMessage

def handle(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )

    if event.message.text == '指令':
        return line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='指令一覽表',
                contents=flex_message.command_list(),
                quick_reply=quick_reply.quick_reply
            )
        )
    if event.message.text == '不查了':
        return line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage( text='好喔', quick_reply=quick_reply.quick_reply )
        )

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='Dummy message',
            contents=flex_message.default_message(),
            quick_reply=quick_reply.quick_reply
        )
    )