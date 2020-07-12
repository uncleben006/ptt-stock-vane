from helper.ptt import calPttSents
from view import quick_reply, flex_message
from config import line_bot_api, redis_url
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction
import re
import redis

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
    if re.search( "^風向(:+)(\d+)(-+)(\d+)(-+)(\d+)(:+)(\d+)(-+)(\d+)(-+)(\d+)", event.message.text ):
        messages = event.message.text.split( ':' )
        start_date = messages[1]
        end_date = messages[2]

        # 先回傳訊息，避免使用者體驗中斷
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text = '謝謝您的查詢，您查詢的時間區間為\n\n' +
                       start_date + '：' + end_date +
                       '\n\n查詢可能需要耗費幾秒鐘的時間，\n請記得點選 「查看結果」。',
                # TODO: 放入 quick_reply.py
                quick_reply = QuickReply(
                    items = [
                        QuickReplyButton( action = PostbackAction( label = "查看結果", data = user_id ) ),
                        QuickReplyButton( action = MessageAction( label = "不看了", text = "不看了" ) ),
                    ]
                )
            )
        )
        # 依照時間區間計算股票版公司情緒並除存在 redis 方便用戶查詢
        r = redis.from_url( redis_url )
        calPttSents( r, user_id, start_date, end_date )
        return


    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='Dummy message',
            contents=flex_message.default_message(),
            quick_reply=quick_reply.quick_reply
        )
    )