
from view import quick_reply
from config import line_bot_api, database_url, s3_bucket
from linebot.models import TextSendMessage
from datetime import datetime
from aws import util
import psycopg2
import requests
from queue import Queue

def handle(event):

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # TODO:把蒐集用戶資料的過程包進 queue 裡優化使用者體驗
    #  q = Queue()
    upsert_user_data( now, profile )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = profile.display_name + ' 您好, 歡迎來到 PTT 股版風向儀，有什麼想知道的事情嗎？',
            quick_reply = quick_reply.quick_reply
        )
    )

# 註解掉，因為目前 S3 bucket 為不公開
# def store_img(profile):
#     with requests.get( profile.picture_url, stream = True ) as r:
#         if r.status_code == 200:
#             with open( "tmp/"+ profile.user_id +".jpg", 'wb' ) as f:
#                 f.write( r.content )

# 把用戶資料存進 heroku postgresql
def upsert_user_data( now, profile ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    sql = "INSERT INTO member \
    VALUES ('{user_id}', '{display_name}', '{picture_url}', '{status_message}', '{follow_datetime}', '{active_datetime}') \
    ON CONFLICT (user_id) DO UPDATE \
    SET picture_url = '{picture_url}', active_datetime = '{active_datetime}' \
    WHERE member.user_id = '{user_id}' "

    sql = sql.format( user_id = profile.user_id,
                      display_name = profile.display_name,
                      picture_url = profile.picture_url,
                      status_message = profile.status_message,
                      follow_datetime = now,
                      active_datetime = now )

    cursor.execute( sql )
    conn.commit()
    cursor.close()
    conn.close()