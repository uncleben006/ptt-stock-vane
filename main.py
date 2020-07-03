

from controller import follow, postback, message
from datetime import datetime, timedelta

from flask import Flask, request, abort

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessage
)

from config import line_bot_api, handler

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index_html():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return '<h1>You have access the server successfully</h1><br>'+dt_string

@app.route("/callback", methods=['POST'])
def callback():

    # line message 的 headers
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        # 將 body 跟 signature 拿來確認消息的合法性
        # 另外還有一個用途，轉發給後續的業務邏輯
        handler.handle( body, signature )
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add( MessageEvent, message=TextMessage )
def handle_message(event):
    message.handle(event)

@handler.add( FollowEvent )
def handle_follow(event):
    follow.handle(event)

@handler.add( PostbackEvent )
def handle_post(event):
    postback.handle(event)

if __name__ == "__main__":
    app.run()