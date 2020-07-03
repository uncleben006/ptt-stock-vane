
from view import quick_reply, flex_message
from config import line_bot_api
from linebot.models import TextSendMessage, MessageAction, QuickReply, QuickReplyButton, FlexSendMessage, DatetimePickerAction
from datetime import date, timedelta

def handle(event):

    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )

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

    # 如果用戶選了起始時間或結束時間，就開始紀錄他輸入的資料，當他兩個都輸入了之後就幫他做查找
    # user 存 start date 再存 end date，如果都能從資料庫取得則 用 start date & end date 回傳 flex message 然後再清掉 context
    # 先把 start date 存進 redis
    if event.postback.data == 'start_date' or event.postback.data == 'end_date':

        return line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='hello',
                contents=flex_message.company_list,
                quick_reply=quick_reply.quick_reply
            )
        )