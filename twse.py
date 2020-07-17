import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re
import time

from helper.util import select_table, insert_table

with open( 'data/company_dict.json', 'r' ) as read_file:
    dict_data = json.load( read_file )


# 如果有匹配字典，就把他們 insert 進 opinion_leader 的 company
def get_company():

    sql = "SELECT target,to_char(date, 'YY-MM-DD'),title,url FROM opinion_leader WHERE company is null;"
    result = select_table(sql)

    refer_company_list = []
    for data in result:
        company = []
        print('data',data[0])
        sql = ''
        for dict in dict_data.items():
            # print( dict[1] )
            for c_name in dict[1]:
                c_name = c_name.replace('*','')
                # print(c_name)
                if re.search( c_name+"+", data[0] ):
                    company.append( dict[1][0] )
                    break
        if company:
            insert_sql = "UPDATE opinion_leader SET company = '"+json.dumps(company, ensure_ascii = False)+"' WHERE url = '"+ data[3] +"';"
            insert_table( insert_sql )
            print( insert_sql )
            print(company)
        else:
            print('no refer company')
        print()

# 不能存超過 1600 行
#
# sql = ''
# for dict in dict_data.items():
#     sql += "alter table company	add \""+dict[0]+"\" float; "
#
# insert_table( sql )

def get_closed_price( date, datas ):
    if datas:
        for data in datas['data']:
            date_str = '109'+'/'+date[4:6]+'/'+date[6:] if date[:4] == '2020' else '108'+'/'+date[4:6]+'/'+date[6:]
            print( date_str )
            print( data[0] )
            if data[0] == date_str:
                date = '2020'+date_str[3:] if date_str[:3] == '109' else '2019'+date_str[:3]
                return data[6],date
    else:
        print('twse api return empty')

# 拿出了作者真正指涉的公司後，就可以依照他們發文指涉的公司，發文的時間，多或空，來爬取對應時間的收盤價，來計算他的投資報酬率
sql = "SELECT company, date, class, url FROM opinion_leader WHERE company is not null;"
result = select_table(sql)

for data in result:

    print(data[1])

    date = data[1].strftime( "%Y%m%d" )

    for stockNo in json.loads(data[0]):

        try:
            url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=' + date + '&stockNo=' + stockNo
            time.sleep(3)
            print(url)
            r = requests.get( url )
            datas = r.json()
            print( datas )
        except Exception as e:
            print(e)
            continue
        if datas['stat'] == '很抱歉，沒有符合條件的資料!':
            # 有一些 twse 會沒有資料，不知道為什麼
            continue

        closed_price,date = get_closed_price( date, datas )
        while not closed_price:
            date = datetime.strptime( date, "%Y%m%d" ) + timedelta( days = 1 )
            date = date.strftime( "%Y%m%d" )
            print( date )
            closed_price = get_closed_price( date )

        print(closed_price,date)



    # upload_date = data['date'].strftime( "%Y%m%d" )
    # # 然後去 twse api 尋找發文 date 是否有在上面，若沒有就增加天數直到找到為止
    #
    #
    # six_days_after = upload_date + timedelta( days = 1 )
