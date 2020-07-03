
# 目標是上傳檔案到 s3
import boto3

# 第一：創建客戶端
try:
    s3_client = boto3.client('s3',
                             aws_access_key_id='AKIAR4NDUH53GWDLQFNM',
                             aws_secret_access_key='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')
    response = s3_client.upload_file('ngrok_is_shit.txt',
                                     'iii-tutorial-v2',
                                     'student08/ngrok_really_shit.txt')
    print(response)
except Exception as e:
    print(e)

# 第二：用客戶端上傳到 s3 的 bucket