import psycopg2
import json
from config import database_url


def upsert_user_data( now, profile ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    sql = "INSERT INTO member \
    VALUES ('{user_id}', '{display_name}', '{picture_url}', '{status_message}', '{follow_datetime}', '{active_datetime}') \
    ON CONFLICT (user_id) DO UPDATE \
    SET picture_url = '{picture_url}', active_datetime = '{active_datetime}' \
    WHERE member.user_id = '{user_id}' "
    print(sql)

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

def get_user_context( profile ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    sql = "SELECT context FROM member WHERE member.user_id = '%s' " % profile.user_id
    print(sql)

    cursor.execute( sql )
    result = cursor.fetchone()
    result = json.loads('"'+result[0]+'"')

    cursor.close()
    conn.close()

    return result

def update_user_context( name, data, profile ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    sql = "UPDATE member SET context='{%s:%s}' WHERE member.user_id = '%s' " % ( name, data, profile.user_id )
    print(sql)

    cursor.execute( sql )
    conn.commit()
    cursor.close()
    conn.close()

def upsert_table( delete_sql, insert_sql ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    cursor.execute( delete_sql )
    cursor.execute( insert_sql )

    conn.commit()
    cursor.close()
    conn.close()

def select_table(sql):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    print(sql)

    cursor.execute( sql )
    result = cursor.fetchall()
    # result = json.loads('"'+result[0]+'"')

    cursor.close()
    conn.close()

    return result

def get_comment(start_date, end_date, company=None):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    sql = "SELECT * FROM company_comment WHERE datetime BETWEEN '"+start_date+"' AND '"+end_date+"'";
    print(sql)

    cursor.execute( sql )
    query_result = cursor.fetchall()

    # query_result = json.loads('"'+query_result[0]+'"')

    cursor.close()
    conn.close()

    if company:
        final_result = []
        for datas in query_result:
            datetime = datas[0]
            comments = datas[1]
            data = [datetime,{company:comments[company]}]
            final_result.append(data)
            # print(final_result)
    else:

        final_result = query_result

    return final_result

# TODO: 思考一下是否要改成 "把評分乘上 總留言比例，以代表整體比例"
def get_sorted_result( result ):

    # 依照 value 來排序字典，篩選掉留言小於 20 的 item
    result = { k:v for k, v in sorted( result.items(), key = lambda item:item[1][0] ) if v[1] > 19 }
    neg_name = list( result.keys() )[:3]
    pos_name = list( result.keys() )[-3:]
    # 回傳前後三個股版留言好感度統計與留言數，並只擷取小數點後兩位
    neg_data = list( result.values() )[:3]
    neg_data = [['%.2f' % elem[0], elem[1]] for elem in neg_data]
    pos_data = list( result.values() )[-3:]
    pos_data = [['%.2f' % elem[0], elem[1]] for elem in pos_data]

    return neg_data, neg_name, pos_data, pos_name