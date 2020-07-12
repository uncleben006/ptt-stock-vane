from helper.ptt import calPttSents
from helper.util import get_sorted_result
from view import quick_reply
from config import line_bot_api, redis_url
from linebot.models import TextSendMessage, MessageAction, QuickReply, QuickReplyButton, DatetimePickerAction, PostbackAction
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

    # 因為 line bot 沒有 cookies & session，所以若要做暫存效果，需要把 start_date & end_date 存入 redis
    # 下面判斷若 redis 裡面有開始與結束時間，則以此時間區間回傳已經儲存在 redis 的公司留言分析結果
    if event.postback.data == 'start_date' or event.postback.data == 'end_date':

        if event.postback.data == 'start_date':
            return r.mset( {'start_date':event.postback.params['date'] } )
        if event.postback.data == 'end_date':
            r.mset( {'end_date':event.postback.params['date']} )

        if r.get( 'start_date' ) and r.get( 'end_date' ):

            # 先回傳訊息，避免使用者體驗中斷
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = '謝謝您的查詢，您查詢的時間區間為\n\n' +
                           r.get( 'start_date' ).decode() + '：' + r.get( 'end_date' ).decode() +
                           '\n\n查詢可能需要耗費幾秒鐘的時間，\n請記得點選 「查看結果」。',
                    quick_reply = QuickReply(
                        items = [
                            QuickReplyButton( action = PostbackAction( label = "查看結果", data = user_id ) ),
                            QuickReplyButton( action = MessageAction( label = "不看了", text = "不看了" ) ),
                        ]
                    )
                )
            )
            # 依照時間區間計算股票版公司情緒並除存在 redis 方便用戶查詢
            calPttSents( r, user_id )

    # 如果 post 過來的是他的 user_id，那就顯示 redis 裡面保存給他的資料
    if event.postback.data == user_id:
        if r.get( user_id ):

            # 依照 value 來排序字典，篩選掉留言小於 20 的結果
            # 回傳前後三個股版留言好感度統計與留言數，並只擷取小數點後兩位
            dict_data, neg_data, neg_name, pos_data, pos_name = get_sorted_result( r, user_id )

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text = '謝謝您的查詢，以下是您的搜尋結果。\n系統會自動替除掉留言少於20的結果\n\n鄉民觀感最好的三間公司：\n' +
                        dict_data[pos_name[0]][1] + '  好感度:' + str(pos_data[2][0]) + '  留言數：' + str(pos_data[2][1]) + '\n' +
                        dict_data[pos_name[1]][1] + '  好感度:' + str(pos_data[1][0]) + '  留言數：' + str(pos_data[1][1]) + '\n' +
                        dict_data[pos_name[2]][1] + '  好感度:' + str(pos_data[0][0]) + '  留言數：' + str(pos_data[0][1]) + '\n\n' +
                        '鄉民觀感最差的公司：\n' +
                        dict_data[neg_name[0]][1] + '  好感度:' + str(neg_data[2][0]) + '  留言數：' + str(neg_data[2][1]) + '\n' +
                        dict_data[neg_name[1]][1] + '  好感度:' + str(neg_data[1][0]) + '  留言數：' + str(neg_data[1][1]) + '\n' +
                        dict_data[neg_name[2]][1] + '  好感度:' + str(neg_data[0][0]) + '  留言數：' + str(neg_data[0][1]) + '\n',
                        quick_reply = quick_reply.quick_reply
                    ),
                    # TODO: 用小輪播顯示三個綠色好公司，三個紅色壞公司，若要查看公司留言，則導入 flask 網站
                    # 所以要額外做一個用來顯示留言的頁面
                    # FlexSendMessage(
                    #     alt_text = '股市風向圖',
                    #     contents = flex_message.company_list(),
                    #     quick_reply = quick_reply.quick_reply
                    # )
                ]
            )

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = '可能還要再等幾秒鐘，搜尋一天大約1～2秒，如果搜尋30天約等30秒上下',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction( label="查看結果", data=user_id )),
                            QuickReplyButton(action=MessageAction(label="不看了", text="不看了")),
                        ]
                    )
                )
            )


