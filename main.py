import json

from controller import follow, postback, message, cron, image
from datetime import datetime

from flask import Flask, request, abort, render_template

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessage,
    ImageMessage
)

from config import handler
from helper.util import get_comment

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index_html():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return '<h1>You have access the server successfully</h1><br>'+dt_string

@app.route('/cron', methods=['GET'])
def cron_job():
    print('start a cron job.')
    cron.job()
    return '<h1>You have finished the cron job successfully</h1>'

@app.route('/comments', methods=['GET'])
def company_comments():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    company = request.args.get('company')

    with open( 'data/company_dict.json', 'r' ) as read_file:
        dict_data = json.load( read_file )

    if start_date and end_date:
        result = get_comment(start_date, end_date, company)
    else:
        return "請輸入時間區間"

    return render_template( "comments.html", result=result, dict_data=dict_data )

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

@handler.add( MessageEvent, message=ImageMessage )
def handle_image_message(event):
    image.handle(event)

@handler.add( FollowEvent )
def handle_follow(event):
    follow.handle(event)

@handler.add( PostbackEvent )
def handle_post(event):
    postback.handle(event)

if __name__ == "__main__":
    app.run()