from helper.ptt import crawlerPtt
from helper.util import upsert_company_comment, get_company_comment
from config import redis_url
import json
import redis
from snownlp import SnowNLP

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
    insert_sql = "INSERT INTO company_comment ( datetime, comment ) VALUES"+values
    delete_sql = "DELETE FROM company_comment"

    upsert_company_comment( delete_sql, insert_sql )

    r = redis.from_url( redis_url )

    # 取出存進 DB 裡的留言，並逐個留言分析，分析這每則留言的分數 (0～1)，並回傳陣列
    # 回傳的陣列就代表 "那一天對那個公司的每則留言之情緒正負"
    # 那用戶若要選取一個時間區間，就會把這些陣列裡面的情緒量化數字加總再除以總數量
    # 得到 "這段時間區間，鄉民對公司所有留言的平均情緒"
    # 藉以得知 "選取的時間區間，鄉民對公司的情緒反應，並顯示給 line 用戶"
    result = get_company_comment()
    for data in result:
        datetime = data[0].strftime( "%Y-%m-%d" )
        # print(datetime)

        for stock_id in data[1]:
            # print(stock_id)
            comments = data[1][stock_id]
            # print(comments)

            # 這邊要把量化的情緒儲存回陣列，並依照用戶選取的時間區段再來加總量化後的情緒再取平均
            # 這麼做是為了避免有公司在某一天有少量的極端評論，影響到總體的情緒平均
            data[1][stock_id] = get_comment_sentiments( comments )

        r.set( "company-"+datetime, json.dumps(data[1]) )
    # print(result)

    # data = json.loads(r.get( "company-2020-07-07" ))
    # print(data)

def get_comment_sentiments( comments ):
    global s
    comment_sentiments = []
    if len( comments ) > 0:
        for comment in comments:
            try:
                s = SnowNLP( u'' + comment + '' )
            except Exception as e:
                print( e )
            print(comment,s.sentiments)
            comment_sentiments.append( s.sentiments )
    return comment_sentiments

