# 首先需要一个能进行回复的机器人框架
import asyncio
from hoshino import Service
from hoshino.util import filt_message

from .. import chara
from . import db_search

sv = Service('pcr_wiki_bydb', help_='''
[角色]简介
[角色]技能
[角色]动作
[角色]羁绊
[角色]数值
             
ps:[]内填写的是角色名称/别称
'''.strip(), bundle='pcr_wiki')

async def get_chara_uid(name, bot, ev):
    uid = chara.name2id(name)
    confi = 100
    guess = False
    if uid == chara.UNKNOWN:
        uid, guess_name, confi = chara.guess_id(name)
        guess = True
        c = chara.fromid(uid)

    if confi < 60:
        return -1

    if guess:
        name = filt_message(name)
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice9Coffee/LandosolRoster'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name} {await c.get_icon_cqcode()} {c.name}'
        await bot.send(ev, msg)
        return -1
    else:
        # unit_id是整形，查找需要末尾加01
        return uid * 100 + 1
        

@sv.on_suffix('简介')
async def chara_intro(bot, ev):
    name = ev.message.extract_plain_text().strip()
    if not name:
        return
    uid = await get_chara_uid(name, bot, ev)
    if uid == -1:
        return
    # 创建查找对象列表
    search_list = [
        'name',
        'talent',
        'guild',
        'brithday',
        'age',
        'height',
        'weight',
        'bloodtype',
        'race',
        'favorite',
        'cv',
        'description']
    # 开始查找
    # 未完待续

    