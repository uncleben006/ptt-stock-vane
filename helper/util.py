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

def upsert_company_command( delete_sql, insert_sql ):

    conn = psycopg2.connect( database_url, sslmode = 'require' )
    cursor = conn.cursor()

    cursor.execute( delete_sql )
    cursor.execute( insert_sql )

    conn.commit()
    cursor.close()
    conn.close()