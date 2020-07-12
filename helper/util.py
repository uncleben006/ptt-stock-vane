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

def upsert_company_comment( delete_sql, insert_sql ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    cursor.execute( delete_sql )
    cursor.execute( insert_sql )

    conn.commit()
    cursor.close()
    conn.close()

def get_company_comment():

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    # sql = "SELECT * FROM company_comment WHERE datetime BETWEEN '2020-07-05' AND '2020-07-07'";
    sql = "SELECT * FROM company_comment";
    print(sql)

    cursor.execute( sql )
    result = cursor.fetchall()
    # result = json.loads('"'+result[0]+'"')

    cursor.close()
    conn.close()

    return result


def get_sorted_result( r, user_id ):
    # r = redis
    result = json.loads( r.get( user_id ) )
    # 依照 value 來排序字典，篩選掉留言小於 20 的 item
    result = { k:v for k, v in sorted( result.items(), key = lambda item:item[1][0] ) if v[1] > 19 }
    neg_name = list( result.keys() )[:3]
    pos_name = list( result.keys() )[-3:]
    # 回傳前後三個股版留言好感度統計與留言數，並只擷取小數點後兩位
    neg_data = list( result.values() )[:3]
    neg_data = [['%.2f' % elem[0], elem[1]] for elem in neg_data]
    pos_data = list( result.values() )[-3:]
    pos_data = [['%.2f' % elem[0], elem[1]] for elem in pos_data]
    with open( 'data/company_dict.json', 'r' ) as read_file:
        dict_data = json.load( read_file )
    return dict_data, neg_data, neg_name, pos_data, pos_name