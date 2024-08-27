# 根据传入的查找对象列表进行查找并返回
import asyncio
import peewee
from zhconv import convert

cn_db_path = r'd:\Code\pcr_wiki_bydb\redive_cn.db'
tw_db_path = r'd:\Code\pcr_wiki_bydb\redive_tw.db'
jp_db_path = r'd:\Code\pcr_wiki_bydb\redive_jp.db'
talent_list = {
    1 : '火',
    2 : '水',
    3 : '风',
    4 : '光',
    5 : '暗',
}

# 创建查找的类别
class Search_Type():
    def __init__(self, uid):
        self.uid = uid

    def _search(self, model, search_type, reture_type, value=None):
        databases = [cn_db, tw_db, jp_db]
        for db in databases:
            try:
                with db.atomic():
                    model._meta.database = db
                    if value is None:
                        query = model.get(getattr(model, 'unit_id') == self.uid)
                    else:
                        query = model.get(getattr(model, search_type) == value)
                    return getattr(query, reture_type)
            except peewee.DoesNotExist:
                continue
        # raise peewee.DoesNotExist(f"Record not found in any database for {model.__name__} with {type}={value}")
    
    # def unit_profile_search(self, type):
    #     query = unit_profile.get(unit_profile.unit_id == self.uid)
    #     return getattr(query, type)

    # def unit_talent_search(self, type):
    #     query = unit_talent.get(unit_talent.unit_id == self.uid)
    #     return getattr(query, type)
    
    # def guild_search(self, type, id):
    #     query = guild.get(guild.guild_id == id)
    #     return getattr(query, type)
    
    def unit_profile_search(self, reture_type, search_type = 'unit_id'):
        return self._search(unit_profile, search_type, reture_type)

    def unit_talent_search(self, reture_type, search_type = 'unit_id'):
        return self._search(unit_talent, search_type, reture_type)

    def guild_search(self, reture_type, value, search_type = 'unit_id'):
        return self._search(guild, search_type, reture_type, value)
    
    def unit_data_search(self, reture_type, search_type = 'unit_id'):
        return self._search(unit_data, search_type, reture_type)

    def name(self):
        return self.unit_profile_search('unit_name')
    
    def talent(self):
        talent = self.unit_talent_search('talent_id')
        return talent_list[talent]

    def guild(self):
        guild_id = self.unit_profile_search('guild_id')
        if not guild_id:
            return '？？？'
        guild_name = self.guild_search('guild_name', guild_id, 'guild_id')
        return guild_name

    def brithday(self):
        return self.unit_profile_search('birth_month') + '月' + self.unit_profile_search('birth_day') + '日'

    def age(self):
        return self.unit_profile_search('age')

    def height(self):
        return self.unit_profile_search('height')

    def weight(self):
        return self.unit_profile_search('weight')

    def bloodtype(self):
        return self.unit_profile_search('blood_type')

    def race(self):
        return self.unit_profile_search('race')

    def favorite(self):
        return self.unit_profile_search('favorite')

    def cv(self):
        return self.unit_profile_search('voice')

    def description(self):
        return self.unit_data_search('comment')

# 数据库连接
cn_db = peewee.SqliteDatabase(cn_db_path)
tw_db = peewee.SqliteDatabase(tw_db_path)
jp_db = peewee.SqliteDatabase(jp_db_path)

# 定义表
class BaseModel(peewee.Model):
    class Meta:
        database = None

class unit_profile(BaseModel):
    unit_id = peewee.IntegerField(primary_key=True)
    unit_name = peewee.CharField()
    age = peewee.CharField()
    guild = peewee.CharField()
    race = peewee.CharField()
    height = peewee.CharField()
    weight = peewee.CharField()
    birth_month = peewee.CharField()
    birth_day = peewee.CharField()
    blood_type = peewee.CharField()
    favorite = peewee.CharField()
    voice = peewee.CharField()
    voice_id = peewee.IntegerField()
    catch_copy = peewee.CharField()
    self_text = peewee.CharField()
    guild_id = peewee.IntegerField()

class unit_talent(BaseModel):
    unit_id = peewee.IntegerField()
    setting_id = peewee.IntegerField(primary_key=True)
    talent_id = peewee.IntegerField()

class guild(BaseModel):
    guild_id = peewee.IntegerField(primary_key=True)
    guild_name = peewee.CharField()
    description = peewee.CharField()
    guild_master = peewee.IntegerField()

class unit_data(BaseModel):
    unit_id = peewee.IntegerField(primary_key=True)
    unit_name = peewee.CharField()
    kana = peewee.CharField()
    prefab_id = peewee.IntegerField()
    prefab_id_battle = peewee.IntegerField()
    is_limited = peewee.IntegerField()
    rarity = peewee.IntegerField()
    motion_type = peewee.IntegerField()
    se_type = peewee.IntegerField()
    move_speed = peewee.IntegerField()
    search_area_width = peewee.IntegerField()
    atk_type = peewee.IntegerField()
    normal_atk_cast_time = peewee.FloatField()
    cutin_1 = peewee.IntegerField()
    cutin_2 = peewee.IntegerField()
    cutin1_star6 = peewee.IntegerField()
    cutin2_star6 = peewee.IntegerField()
    guild_id = peewee.IntegerField()
    exskill_display = peewee.IntegerField()
    comment = peewee.CharField()
    only_disp_owned = peewee.IntegerField()
    start_time = peewee.CharField()
    end_time = peewee.CharField()
    original_unit_id = peewee.IntegerField()

# 测试
if __name__ == '__main__':
    uid = 131801
    search_list = ['name', 'guild', 'talent', 'brithday', 'age',
                   'height', 'weight', 'bloodtype', 'race', 'favorite', 'cv', 'description']
    search_obj = Search_Type(uid)
    for search in search_list:
        print(convert(getattr(search_obj, search)(),'zh-cn'))