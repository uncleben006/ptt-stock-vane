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
        condition = messages[0]
        print(condition)
        start_date = messages[-2]
        end_date = messages[-1]

        if condition == '風向':
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
            # 依照時間區間計算股票版公司情緒並除存在 redis 方便用戶查詢
            company = None
            r = redis.from_url( redis_url )
            calPttSents( r, user_id, start_date, end_date, company )
            return
        elif condition == '留言':
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = '前往查看公司評論',
                    contents = flex_message.company_comment( start_date, end_date ),
                    quick_reply = quick_reply.quick_reply()
                )
            )
            return
        else:
            with open( 'data/company_dict.json', 'r' ) as read_file:
                dict_data = json.load( read_file )

            select = condition.split('_')[0]
            company = condition.split( '_' )[1]
            for company_refers in dict_data.items():
                if company in company_refers[1]:
                    company = company_refers[0]

            if select == '評價':
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
                r = redis.from_url( redis_url )
                calPttSents( r, user_id, start_date, end_date, company )
                return
            if select == '留言':
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text = '前往查看公司評論',
                        contents = flex_message.company_comment( start_date, end_date, company ),
                        quick_reply = quick_reply.quick_reply()
                    )
                )
                return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = '點選快速查詢風向：\n查詢 PTT 股版的留言情緒量化結果\n\n'
                   '點選快速查詢留言：\n查詢 PTT 股版的留言\n\n'
                   '也可以輸入「指令」查詢',
            quick_reply = quick_reply.quick_reply()
        )
    )