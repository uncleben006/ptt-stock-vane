from datetime import timedelta,date

today = date.today()

from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction,
    PostbackAction,
    DatetimePickerAction
)

quick_reply = QuickReply(
    items=[
        # QuickReplyButton(action=DatetimePickerAction( label="快速查詢風向", data="stock_company_list", mode="date", initial=str(today), max=str(today), min=str(today - timedelta(days=30)) ) ),
        QuickReplyButton(action=PostbackAction( label="快速查詢風向", data="stock_company_list" ) ),
        QuickReplyButton(action=MessageAction(label="意見領袖報酬率", text="查詢公司名稱或代號")),
        QuickReplyButton(action=MessageAction(label="指令", text='指令')),
    ]
)