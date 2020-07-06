from helper.util import upsert_user_data
from view import quick_reply
from config import line_bot_api
from linebot.models import TextSendMessage
from datetime import datetime

def handle(event):

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = profile.display_name + ' 您好, 歡迎來到 PTT 股版風向儀，有什麼想知道的事情嗎？',
            quick_reply = quick_reply.quick_reply
        )
    )

    upsert_user_data( now, profile )