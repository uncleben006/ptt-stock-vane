import boto3
from view import quick_reply
from config import line_bot_api, s3_access_key_id, s3_secret_access_key, s3_bucket
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from datetime import date

def handle(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile( user_id )
    today = date.today()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text = '你傳什麼照蛤？我要把他偷偷存起來！',
            quick_reply = QuickReply( items = [ QuickReplyButton( action = MessageAction(label="好吧", text='好吧') ) ] )
        )
    )

    image_temp_variable = line_bot_api.get_message_content((event.message.id))

    with open('/tmp/'+event.message.id + '.jpg', 'wb') as f:
        for chunk in image_temp_variable.iter_content():
            f.write(chunk)

    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key_id, aws_secret_access_key=s3_secret_access_key )
    s3_client.upload_file( '/tmp/'+event.message.id + '.jpg', s3_bucket, 'student08/'+event.message.id + '.jpg' )