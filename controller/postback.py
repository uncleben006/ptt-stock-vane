from helper.ptt import calPttSents
from helper.util import get_sorted_result
from view import quick_reply, flex_message
from config import line_bot_api, redis_url
from linebot.models import TextSendMessage, FlexSendMessage
from datetime import date
import redis
import json
import re
import query_string

from view.quick_reply import search_date, query_date


def handle(event):

    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )
    r = redis.from_url( redis_url )

    today = date.today ()

    # if re.search( "^action=opinion_leader", event.postback.data ):
    #     post_data = query_string.parse(event.postback.data)
    #     print(post_data)

    # if event.postback.data == 'opinion_leader_list':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(
    #             text = '請輸入時間',
    #             quick_reply = query_date( [6,12,30,60],user_id )
    #         )
    #     )
        # 若 user 查詢意見領袖投資報酬率時，詢問 user 要依照多久時間為指標各個作者的投資報酬率
        # select (company_name,date) from opinion_leader 會回傳一個 list with company_id and date
        # 用這個 list 去 query 出 company_price => select company_id from company_price where date = (date + user_insert_date)
        # 上面這個 query 會跑 3000 多個，勢必會對使用者體驗造成負擔，所以也要做二段訊息讓資訊緩衝，先把 query 結果存在 redis
        # user 點選查看結果後才會回傳真正的結果
        # 若 user 查詢某特定 id 的

    if event.postback.data == 'company_comment_list':
        r.delete('select')
        r.set('select', 'comment')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請輸入時間',
                quick_reply= search_date( today )
            )
        )

    # 查詢自那天起的股市留言歸納出前後三名公司，做成 Flex message 送給用戶
    if event.postback.data == 'company_sentiment_list':
        r.delete( 'select' )
        r.set( 'select', 'sentiment' )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請輸入時間',
                quick_reply= search_date( today )
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

            if r.get('select').decode() == 'comment':
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(
                            text = "感謝您的查詢，點選以下網址查看留言\n https://ptt-stock-vane.herokuapp.com/comments?start_date="+r.get( 'start_date' ).decode()+"&end_date="+r.get( 'end_date' ).decode()+"&company=",
                            quick_reply = quick_reply.quick_reply()
                        )
                        # FlexSendMessage(
                        #     alt_text = '前往查看公司評論',
                        #     contents = flex_message.company_comment( r.get( 'start_date' ).decode(), r.get( 'end_date' ).decode() ),
                        #     quick_reply = quick_reply.quick_reply()
                        # )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text = '謝謝您的查詢，您查詢的時間區間為\n\n' +
                               r.get( 'start_date' ).decode() + '：' + r.get( 'end_date' ).decode() +
                               '\n\n查詢可能需要耗費幾秒鐘的時間，\n請記得點選 「查看結果」。',
                        quick_reply = quick_reply.get_result( user_id )
                    )
                )
                if r.get('select').decode() == 'sentiment':
                    # 依照時間區間計算股票版公司情緒並除存在 redis 方便用戶查詢
                    calPttSents( r, user_id, r.get( 'start_date' ).decode(), r.get( 'end_date' ).decode() )

            r.delete( 'end_date' )
            r.delete( 'start_date' )

    # 如果 post 過來的是他的 user_id，那就顯示 redis 裡面保存給他的資料
    if event.postback.data == user_id:
        if r.get( user_id ):

            with open( 'data/company_dict.json', 'r' ) as read_file:
                dict_data = json.load( read_file )

            result = json.loads( r.get( user_id ) )

            # 若用戶只查一個公司，就回覆一個公司的情緒分析
            if len(result.keys()) == 1:
                print(result)
                company_id = list(result.keys())[0]
                company_name = dict_data[company_id][1]
                sentiment = '%.2f' % list(result.values())[0][0]
                comment = list(result.values())[0][1]
                return line_bot_api.reply_message(
                    event.reply_token,
                    [
                        # TODO: 用 Flex message 取代
                        TextSendMessage(
                            text = '謝謝您的查詢，以下是您的搜尋結果。\n'+ company_name + ' '+ company_id +
                                   '\n好感度：' + str(sentiment) +
                                   '\n留言數：' + str(comment),
                            quick_reply = quick_reply.quick_reply()
                        )
                    ]
                )

            # 依照 value 來排序字典，篩選掉留言小於 20 的結果
            # 回傳前後三個股版留言好感度統計與留言數，並只擷取小數點後兩位
            neg_data, neg_name, pos_data, pos_name = get_sorted_result( result )

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text = '謝謝您的查詢，以下是您的搜尋結果。\n系統會自動替除掉留言少於20的結果\n\n鄉民觀感最好的三間公司：\n' +
                        dict_data[pos_name[2]][1] + '  好感度:' + str(pos_data[2][0]) + '  留言數：' + str(pos_data[2][1]) + '\n' +
                        dict_data[pos_name[1]][1] + '  好感度:' + str(pos_data[1][0]) + '  留言數：' + str(pos_data[1][1]) + '\n' +
                        dict_data[pos_name[0]][1] + '  好感度:' + str(pos_data[0][0]) + '  留言數：' + str(pos_data[0][1]) + '\n\n' +
                        '鄉民觀感最差的公司：\n' +
                        dict_data[neg_name[2]][1] + '  好感度:' + str(neg_data[2][0]) + '  留言數：' + str(neg_data[2][1]) + '\n' +
                        dict_data[neg_name[1]][1] + '  好感度:' + str(neg_data[1][0]) + '  留言數：' + str(neg_data[1][1]) + '\n' +
                        dict_data[neg_name[0]][1] + '  好感度:' + str(neg_data[0][0]) + '  留言數：' + str(neg_data[0][1]) + '\n',
                        quick_reply = quick_reply.quick_reply()
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
                    quick_reply = quick_reply.get_result( user_id )
                )
            )