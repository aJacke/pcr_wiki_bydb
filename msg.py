# 对db_search.py的消息处理并传回main.py
import asyncio
import os
import peewee
from zhconv import convert

from . import db_search

script_path = os.path.dirname(os.path.abspath(__file__))
cn_db_path = os.path.join(script_path,'redive_cn.db')
tw_db_path = os.path.join(script_path,'redive_tw.db')
jp_db_path = os.path.join(script_path,'redive_jp.db')

cn_db = peewee.SqliteDatabase(cn_db_path)
tw_db = peewee.SqliteDatabase(tw_db_path)
jp_db = peewee.SqliteDatabase(jp_db_path)

def msg_process(uid, search_list):
    search_obj = db_search.Search_Type(uid, cn_db, tw_db, jp_db)
    result = ''
    for search in search_list:
        result += convert(getattr(search_obj, search)(),'zh-cn')
    return result

if __name__ == '__main__':
    uid = 131801
    search_list = ['name', 'guild', 'talent', 'brithday', 'age',
                   'height', 'weight', 'bloodtype', 'race', 'favorite', 'cv', 'description']
    result = msg_process(uid, search_list)
    print(result)