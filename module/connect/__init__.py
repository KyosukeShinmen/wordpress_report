# coding: UTF-8
import pymysql.cursors
import re
import json
import configparser

def repeatQuery(pattern, counter, separate = ","):
    array = [pattern for x in range(counter)]
    return separate.join(array)

class mysql():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        conn = pymysql.connect(
            host = config['DB']['host'],
            user = config['DB']['user'],
            db = config['DB']['table_name'],
            password = config['DB']['password'],
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )
        self.dbh = conn
        self.prefix = config['DB']['prefix']

    def getPost(self, postType: str = 'post', limit: int = 0):
        with self.dbh.cursor() as cursor:
            sql = f"SELECT * FROM {self.prefix}_posts WHERE post_status = 'publish' AND post_type = %s {f'LIMIT {limit}' if limit != 0 else ''};"
            cursor.execute(sql,(postType))
            items = cursor.fetchall()
            return items

    def getPostMeta(self, post_id: int, meta_key: str):
        with self.dbh.cursor() as cursor:
            sql = f"SELECT meta_value FROM {self.prefix}_postmeta WHERE post_id = %s AND meta_key = %s;"
            cursor.execute(sql,(post_id, meta_key))
            item = cursor.fetchone()
            if item is not None:
                return item["meta_value"].decode("utf-8")
            else:
                return None

    def select(self, sql: str):
        with self.dbh.cursor() as cursor:
            cursor.execute(sql)
            item = cursor.fetchall()
            return item

    def prepared(self, sql: str, query: list):
        with self.dbh.cursor() as cursor:
            cursor.execute(sql,query)
            item = cursor.fetchall()
            return item