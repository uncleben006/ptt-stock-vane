from datetime import timedelta

from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction,
    PostbackAction,
    DatetimePickerAction, URIAction
)

def quick_reply():
    return QuickReply(
        items=[
            # QuickReplyButton(action=DatetimePickerAction( label="快速查詢風向", data="stock_company_list", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)) ) ),
            QuickReplyButton(action=PostbackAction( label="快速查詢風向", data="company_sentiment_list" ) ),
            QuickReplyButton(action=PostbackAction( label="快速查詢留言", data="company_comment_list") ),
            QuickReplyButton(action=MessageAction(label="指令", text='指令')),
        ]
    )


def get_result( user_id ):
    return QuickReply(
        items = [
            QuickReplyButton( action = PostbackAction( label = "查看結果", data = user_id ) ),
            QuickReplyButton( action = MessageAction( label = "不看了", text = "不看了" ) ),
        ]
    )

def search_date( today ):
    return QuickReply(
        items = [
            QuickReplyButton( action = DatetimePickerAction(
                label = "起始時間",
                data = "start_date",
                mode = "date",
                initial = str( today ),
                max = str( today ),
                min = str( today - timedelta( days = 30 ) )
            ) ),
            QuickReplyButton( action = DatetimePickerAction(
                label = "結束時間",
                data = "end_date",
                mode = "date",
                initial = str( today ),
                max = str( today ),
                min = str( today - timedelta( days = 30 ) )
            ) ),
            QuickReplyButton( action = MessageAction(
                label = "不查了",
                text = "不查了"
            ) ),
        ]
    )

def query_date( query_date,user_id ):
    items = []
    for date in query_date:
        print(date)
        items.append(
            QuickReplyButton(
                action = PostbackAction(
                    label = str(date)+" 天", data = "action=opinion_leader&date="+str(date)+"&user_id="+user_id+""
                )
            ) ),

    items.append( QuickReplyButton( action = MessageAction( label = "不查了", text = "不查了" ) ) )

    return QuickReply(
        items = items
    )