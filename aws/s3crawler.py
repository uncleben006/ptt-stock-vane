'''

爬蟲爬網頁並存到 S3 去

'''

import requests
import boto3

boto3.setup_default_session(profile_name='tibame_s3')

response = requests.get('https://www.toutiao.com/')

text_file = open('sample.html','w', encoding='utf8')
text_file.write(response.text)
text_file.close()

s3_client = boto3.client('s3')
response = s3_client.upload_file('sample.html',
                                 'iii-tutorial-v2',
                                 'student08/sample.html')
print(response)

# 用戶從 s3 下載檔案
s3_client.download_file('iii-tutorial-v2', 'student08/sample.html', 'test.html')