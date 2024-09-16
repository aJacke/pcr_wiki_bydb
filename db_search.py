# 根据传入的查找对象列表进行查找并返回
import asyncio
import peewee
from zhconv import convert

from . import skill_action as sa, chara_stats_calculator as csc

talent_list = {
    1 : '火',
    2 : '水',
    3 : '风',
    4 : '光',
    5 : '暗',
}

# 默认角色
default_unit_lvl = 316

# 创建查找的类别
class Search_Type():
    def __init__(self, uid, cn_db, tw_db, jp_db):
        self.uid = uid
        self.cn_db = cn_db
        self.tw_db = tw_db
        self.jp_db = jp_db
        self.chara_dict = {}

    def _search(self, model, search_type, return_type, value=None):
        databases = [self.cn_db, self.tw_db, self.jp_db]
        for db in databases:
            try:
                with db.atomic():
                    model._meta.database = db
                    if value is None:
                        query = model.get(getattr(model, 'unit_id') == self.uid)
                    else:
                        query = model.get(getattr(model, search_type) == value)
                    return getattr(query, return_type)
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
    
    def unit_profile_search(self, return_type, search_type = 'unit_id'):
        return self._search(unit_profile, search_type, return_type)

    def unit_talent_search(self, return_type, search_type = 'unit_id'):
        return self._search(unit_talent, search_type, return_type)

    def guild_search(self, return_type, value, search_type = 'unit_id'):
        return self._search(guild, search_type, return_type, value)
    
    def unit_data_search(self, return_type, search_type = 'unit_id'):
        return self._search(unit_data, search_type, return_type)
    
    def unit_skill_data_search(self, return_type, search_type = 'unit_id'):
        return self._search(unit_skill_data, search_type, return_type)
    
    def skill_data_search(self, return_type, value, search_type = 'skill_id'):
        return self._search(skill_data, search_type, return_type, value)
    
    def skill_action_search(self, return_type, value, search_type = 'action_id'):
        return self._search(skill_action, search_type, return_type, value)

    def name(self):
        return '名称：' + self.unit_profile_search('unit_name')
    
    def talent(self):
        talent = self.unit_talent_search('talent_id')
        return '属性：' + talent_list[talent]

    def guild(self):
        guild_id = self.unit_profile_search('guild_id')
        if not guild_id:
            return '公会：？？？'
        guild_name = self.guild_search('guild_name', guild_id, 'guild_id')
        return '公会：' + guild_name

    def brithday(self):
        return '生日：' + self.unit_profile_search('birth_month') + '月' + self.unit_profile_search('birth_day') + '日'

    def age(self):
        return '年龄：' + self.unit_profile_search('age')

    def height(self):
        return '身高：' + self.unit_profile_search('height')

    def weight(self):
        return '体重：' + self.unit_profile_search('weight')

    def bloodtype(self):
        return '血型：' + self.unit_profile_search('blood_type')

    def race(self):
        return '种族：' + self.unit_profile_search('race')

    def favorite(self):
        return '爱好：' + self.unit_profile_search('favorite')

    def cv(self):
        return '声优：' + self.unit_profile_search('voice')

    def description(self):
        return '简介：' + self.unit_data_search('comment').replace('\n', '')

    def skill_ub(self): # Union Burst
        # 常规ub和6星强化ub
        union_burst_list = ['union_burst', 'union_burst_evolution']
        ub_result = '\n============================='
        for skill_type in union_burst_list:
            skill_id = self.unit_skill_data_search(skill_type)
            if not skill_id:
                continue
            icon_type = self.skill_data_search('icon_type', skill_id)
            skill_name = self.skill_data_search('name', skill_id)
            skill_desc = self.skill_data_search('description', skill_id)
            skill_desc = skill_desc.replace('\n', '')
            ub_result += f'img:{icon_type}'
            if skill_type == 'union_burst':
                ub_result += f'UB：{skill_name}\n描述：\n{skill_desc}'
                ub_result += self.skill_action(skill_id)
            else:
                ub_result += f'6星UB：{skill_name}\n描述：\n{skill_desc}'
                ub_result += self.skill_action(skill_id)
        return ub_result
    
    def skill_ms(self): # Main Skill
        # 主动技能和专武强化技能
        main_skill_list = ['main_skill_1', 'main_skill_evolution_1', 'main_skill_2', 'main_skill_evolution_2']
        ms_result = '\n============================='
        for skill_type in main_skill_list:
            skill_id = self.unit_skill_data_search(skill_type)
            if not skill_id:
                continue
            icon_type = self.skill_data_search('icon_type', skill_id)
            skill_name = self.skill_data_search('name', skill_id)
            skill_desc = self.skill_data_search('description', skill_id)
            skill_desc = skill_desc.replace('\n', '')
            ms_result += f'img:{icon_type}'
            if 'evolution' in skill_type:
                ms_result += f'专武强化技能{skill_type[-1]}：{skill_name}\n描述：\n{skill_desc}'
                ms_result += self.skill_action(skill_id)
            else:
                ms_result += f'技能{skill_type[-1]}：{skill_name}\n描述：\n{skill_desc}'
                ms_result += self.skill_action(skill_id)
        return ms_result
            
    def skill_ex(self): # Ex Skill
        # ex技能和5星强化ex技能
        ex_skill_list = ['ex_skill_1', 'ex_skill_evolution_1']
        ex_result = '\n============================='
        for skill_type in ex_skill_list:
            skill_id = self.unit_skill_data_search(skill_type)
            if not skill_id:
                continue
            icon_type = self.skill_data_search('icon_type', skill_id)
            skill_name = self.skill_data_search('name', skill_id)
            skill_desc = self.skill_data_search('description', skill_id)
            skill_desc = skill_desc.replace('\n', '')
            ex_result += f'img:{icon_type}'
            if skill_type == 'ex_skill_1':
                ex_result += f'ex技能：{skill_name}\n描述：\n{skill_desc}'
                ex_result += self.skill_action(skill_id)
            else:
                ex_result += f'5星强化ex技能：{skill_name}\n描述：\n{skill_desc}'
                ex_result += self.skill_action(skill_id)
        return ex_result
    
    def skill_sp(self): # SP Skill
        # sp技能
        sp_skill_list = ['sp_skill_1','sp_skill_2','sp_skill_3','sp_skill_4','sp_skill_5']
        sp_result = ''
        for skill_type in sp_skill_list:
            skill_id = self.unit_skill_data_search(skill_type)
            if not skill_id:
                continue
            icon_type = self.skill_data_search('icon_type', skill_id)
            skill_name = self.skill_data_search('name', skill_id)
            skill_desc = self.skill_data_search('description', skill_id)
            skill_desc = skill_desc.replace('\n', '')
            sp_result += f'img:{icon_type}'
            sp_result += f'sp技能{skill_type[-1]}：{skill_name}\n描述：\n{skill_desc}'
            sp_result += self.skill_action(skill_id)
        if sp_result == '':
            return ''
        sp_result = '\n=============================' + sp_result
        return sp_result
    
    def chara_stats(self, search_list):
        n, chara_stats_dict = csc.chara_calculator(self.uid, self.cn_db, self.tw_db, self.jp_db, default_unit_lvl).calculate_all_value()
        for search_type in search_list:
            self.chara_dict[search_type] = chara_stats_dict[search_type]
        return self.chara_dict

    def skill_action_list_search(self, action_id):
        skill_action_list = {}
        skill_action_list['action_type'] = self.skill_action_search('action_type', action_id)
        skill_action_list['action_detail_1'] = self.skill_action_search('action_detail_1', action_id)
        skill_action_list['action_detail_2'] = self.skill_action_search('action_detail_2', action_id)
        skill_action_list['action_detail_3'] = self.skill_action_search('action_detail_3', action_id)
        skill_action_list['action_value_1'] = self.skill_action_search('action_value_1', action_id)
        skill_action_list['action_value_2'] = self.skill_action_search('action_value_2', action_id)
        skill_action_list['action_value_3'] = self.skill_action_search('action_value_3', action_id)
        skill_action_list['action_value_4'] = self.skill_action_search('action_value_4', action_id)
        skill_action_list['action_value_5'] = self.skill_action_search('action_value_5', action_id)
        skill_action_list['action_value_6'] = self.skill_action_search('action_value_6', action_id)
        skill_action_list['action_value_7'] = self.skill_action_search('action_value_7', action_id)
        skill_action_list['target_assignment'] = self.skill_action_search('target_assignment', action_id)
        skill_action_list['target_area'] = self.skill_action_search('target_area', action_id)
        skill_action_list['target_range'] = self.skill_action_search('target_range', action_id)
        skill_action_list['target_type'] = self.skill_action_search('target_type', action_id)
        skill_action_list['target_number'] = self.skill_action_search('target_number', action_id)
        skill_action_list['target_count'] = self.skill_action_search('target_count', action_id)
        skill_action_list['description'] = self.skill_action_search('description', action_id)
        skill_action_list['level_up_disp'] = self.skill_action_search('level_up_disp', action_id)
        return skill_action_list
    
    def skill_action(self, skill_id):
        action_id_list = []
        depend_action_dict = {}
        for i in range(1, 11):
            action_id = self.skill_data_search(f'action_{i}', skill_id)
            if not action_id:
                break
            depend_action_id = self.skill_data_search(f'depend_action_{i}', skill_id)
            if depend_action_id:
                depend_action_dict[action_id] = depend_action_id
            action_id_list.append(action_id)
        if not action_id_list:
            return f'什么都没找到，请至github上提交issue，技能ID：{skill_id}'
        skill_action_result = '\n效果：'
        self.chara_stats(['atk', 'magic_str'])
        for action_id in action_id_list:
            skill_action_result += '\n'
            sal = self.skill_action_list_search(action_id)
            sac = sa.SkillAction(action_id, sal['action_detail_1'], sal['action_detail_2'], sal['action_detail_3'], sal['action_value_1'], 
                     sal['action_value_2'], sal['action_value_3'], sal['action_value_4'], sal['action_value_5'], sal['action_value_6'], sal['action_value_7'], 
                     sal['target_assignment'], sal['target_area'], sal['target_range'], sal['target_type'], sal['target_number'], sal['target_count'], 
                     sal['description'], sal['level_up_disp'], default_unit_lvl, self.chara_dict['atk'], self.chara_dict['magic_str'], depend_action_dict[action_id] if action_id in depend_action_dict else None)
            skill_action_result += sac.action_type(sal['action_type'])
        return skill_action_result

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

class unit_skill_data(BaseModel):
    unit_id = peewee.IntegerField(primary_key=True)
    union_burst = peewee.IntegerField()
    main_skill_1 = peewee.IntegerField()
    main_skill_2 = peewee.IntegerField()
    main_skill_3 = peewee.IntegerField()
    main_skill_4 = peewee.IntegerField()
    main_skill_5 = peewee.IntegerField()
    main_skill_6 = peewee.IntegerField()
    main_skill_7 = peewee.IntegerField()
    main_skill_8 = peewee.IntegerField()
    main_skill_9 = peewee.IntegerField()
    main_skill_10 = peewee.IntegerField()
    ex_skill_1 = peewee.IntegerField()
    ex_skill_evolution_1 = peewee.IntegerField()
    ex_skill_2 = peewee.IntegerField()
    ex_skill_evolution_2 = peewee.IntegerField()
    ex_skill_3 = peewee.IntegerField()
    ex_skill_evolution_3 = peewee.IntegerField()
    ex_skill_4 = peewee.IntegerField()
    ex_skill_evolution_4 = peewee.IntegerField()
    ex_skill_5 = peewee.IntegerField()
    ex_skill_evolution_5 = peewee.IntegerField()
    sp_union_burst = peewee.IntegerField()
    sp_skill_1 = peewee.IntegerField()
    sp_skill_2 = peewee.IntegerField()
    sp_skill_3 = peewee.IntegerField()
    sp_skill_4 = peewee.IntegerField()
    sp_skill_5 = peewee.IntegerField()
    union_burst_evolution = peewee.IntegerField()
    main_skill_evolution_1 = peewee.IntegerField()
    main_skill_evolution_2 = peewee.IntegerField()
    sp_skill_evolution_1 = peewee.IntegerField()
    sp_skill_evolution_2 = peewee.IntegerField()

class skill_data(BaseModel):
    skill_id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    skill_type = peewee.IntegerField()
    skill_area_width = peewee.IntegerField()
    skill_cast_time = peewee.FloatField()
    boss_ub_cool_time = peewee.FloatField()
    action_1 = peewee.IntegerField()
    action_2 = peewee.IntegerField()
    action_3 = peewee.IntegerField()
    action_4 = peewee.IntegerField()
    action_5 = peewee.IntegerField()
    action_6 = peewee.IntegerField()
    action_7 = peewee.IntegerField()
    action_8 = peewee.IntegerField()
    action_9 = peewee.IntegerField()
    action_10 = peewee.IntegerField()
    depend_action_1 = peewee.IntegerField()
    depend_action_2 = peewee.IntegerField()
    depend_action_3 = peewee.IntegerField()
    depend_action_4 = peewee.IntegerField()
    depend_action_5 = peewee.IntegerField()
    depend_action_6 = peewee.IntegerField()
    depend_action_7 = peewee.IntegerField()
    depend_action_8 = peewee.IntegerField()
    depend_action_9 = peewee.IntegerField()
    depend_action_10 = peewee.IntegerField()
    description = peewee.CharField()
    icon_type = peewee.IntegerField()

class skill_action(BaseModel):
    action_id = peewee.IntegerField(primary_key=True)
    class_id = peewee.IntegerField()
    action_type = peewee.IntegerField()
    action_detail_1 = peewee.IntegerField()
    action_detail_2 = peewee.IntegerField()
    action_detail_3 = peewee.IntegerField()
    action_value_1 = peewee.FloatField()
    action_value_2 = peewee.FloatField()
    action_value_3 = peewee.FloatField()
    action_value_4 = peewee.FloatField()
    action_value_5 = peewee.FloatField()
    action_value_6 = peewee.FloatField()
    action_value_7 = peewee.FloatField()
    target_assignment = peewee.IntegerField()
    target_area = peewee.IntegerField()
    target_range = peewee.IntegerField()
    target_type = peewee.IntegerField()
    target_number = peewee.IntegerField()
    target_count = peewee.IntegerField()
    description = peewee.CharField()
    level_up_disp = peewee.CharField()

# 测试
if __name__ == '__main__':
    uid = 131801
    search_list = ['name', 'guild', 'talent', 'brithday', 'age',
                   'height', 'weight', 'bloodtype', 'race', 'favorite', 'cv', 'description']
    search_obj = Search_Type(uid)
    for search in search_list:
        print(convert(getattr(search_obj, search)(),'zh-cn'))