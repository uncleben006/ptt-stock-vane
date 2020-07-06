from helper.util import get_user_context, update_user_context
from view import quick_reply, flex_message
from config import line_bot_api, redis_url
from linebot.models import TextSendMessage, MessageAction, QuickReply, QuickReplyButton, FlexSendMessage, DatetimePickerAction
from datetime import date, timedelta
import redis

def handle(event):

    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )
    r = redis.from_url( redis_url )

    today = date.today ()

    # 查詢自那天起的股市留言歸納出前後三名公司，做成 Flex message 送給用戶
    if event.postback.data == 'stock_company_list':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請輸入時間',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=DatetimePickerAction( label="起始時間", data="start_date", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)) ) ),
                        QuickReplyButton(action=DatetimePickerAction(label="結束時間", data="end_date", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)))),
                        QuickReplyButton(action=MessageAction(label="不查了", text="不查了")),
                    ]
                )
            )
        )

    # 把 start_date & end_date 存入 redis 做暫存，若兩個值都有則開始爬蟲並回傳結果
    if event.postback.data == 'start_date' or event.postback.data == 'end_date':

        if event.postback.data == 'start_date':
            r.mset( {'start_date':event.postback.params['date'] } )
        if event.postback.data == 'end_date':
            r.mset( {'end_date':event.postback.params['date']} )

        if r.get( 'start_date' ) and r.get( 'end_date' ):
            # 在這裡做爬蟲，回傳結果
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = '您查詢的時間區間\n'+ r.get( 'start_date' ).decode() +'：'+ r.get( 'end_date' ).decode(),
                    quick_reply = QuickReply(
                        items=[
                            QuickReplyButton(action=DatetimePickerAction( label="起始時間", data="start_date", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)) ) ),
                            QuickReplyButton(action=DatetimePickerAction(label="結束時間", data="end_date", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)))),
                            QuickReplyButton(action=MessageAction(label="不查了", text="不查了")),
                        ]
                    )
                )
            )
            r.delete( 'end_date' )
            r.delete( 'start_date' )
