from helper.ptt import crawlerPtt
from helper.util import upsert_company_command
import json

def job():

    # 實例化爬蟲 輸入爬取看板
    url = 'https://www.ptt.cc/bbs/Stock/index.html'
    date_limit = 30
    stock = crawlerPtt(url,date_limit)

    # 爬取完成，顯示出所有留言字典
    print( stock.messageDict )

    values = ''
    for date in stock.messageDict:
        values = values + "( '" + date + "' , '" + json.dumps(stock.messageDict[date], ensure_ascii=False) + "' ),"
    values = values[:-1]
    insert_sql = "INSERT INTO company_command ( datetime, command ) VALUES"+values
    delete_sql = "DELETE FROM company_command"

    upsert_company_command( delete_sql, insert_sql )