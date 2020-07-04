from linebot import LineBotApi, WebhookHandler
import os

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

database_url = os.getenv('DATABASE_URL')
redis_url = os.getenv('REDIS_URL')

s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
s3_bucket = os.getenv('S3_BUCKET')

iam_access_key_id = os.getenv('IAM_ACCESS_KEY_ID')
iam_secret_access_key = os.getenv('IAM_SECRET_ACCESS_KEY')