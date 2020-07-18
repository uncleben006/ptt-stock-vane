from helper.ptt import calPttSents
from view import quick_reply, flex_message
from config import line_bot_api, redis_url
from linebot.models import TextSendMessage, FlexSendMessage
from datetime import date
import re
import redis
import json

def handle(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )
    today = date.today()

    if event.message.text == '指令':
        return line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='指令一覽表',
                contents=flex_message.command_list(today),
                quick_reply=quick_reply.quick_reply()
            )
        )
    if event.message.text == '不查了' or event.message.text == '不看了':
        return line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage( text='好喔', quick_reply=quick_reply.quick_reply() )
        )
    # 如果匹配 ^[自首隨意][:][數字][-][數字][-][數字][:][數字][-][數字][-][數字]$
    # ^:自首必填，$:字尾必為數字
    if re.search( "^([\s\S]+)(:+)(\d+)(-+)(\d+)(-+)(\d+)(:+)(\d+)(-+)(\d+)(-+)(\d+)$", event.message.text ):

        messages = event.message.text.split( ':' )
        company = messages[0]
        start_date = messages[1]
        end_date = messages[2]

        # 先回傳訊息，避免使用者體驗中斷
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text = '謝謝您的查詢，您查詢的時間區間為\n\n' +
                       start_date + '：' + end_date +
                       '\n\n查詢可能需要耗費幾秒鐘的時間，\n請記得點選 「查看結果」。',
                quick_reply = quick_reply.get_result( user_id )
            )
        )

        if company == '風向':
            company = None
        else:
            with open( 'data/company_dict.json', 'r' ) as read_file:
                dict_data = json.load( read_file )

            for company_refers in dict_data.items():
                if company in company_refers[1]:
                    company = company_refers[0]

        # print(company)

        # 依照時間區間計算股票版公司情緒並除存在 redis 方便用戶查詢
        r = redis.from_url( redis_url )
        calPttSents( r, user_id, start_date, end_date, company )
        return


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = '請輸入正確指令以查詢資訊，若不清楚可以點選「指令」查詢有什麼指令可以使用',
            quick_reply = quick_reply.quick_reply()
        )
    )