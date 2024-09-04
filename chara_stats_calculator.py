import peewee

class chara_calculator:
    def __init__(self, unit_id, level, rank, star, unique_level, ex_level, cn_db, tw_db, jp_db):
        self.unit_id = unit_id
        self.level = level
        self.rank = rank
        self.star = star
        self.unique_level = unique_level
        self.ex_level = ex_level
        self.cn_db = cn_db
        self.tw_db = tw_db
        self.jp_db = jp_db
    
    def _search(self, model, search_type, return_type, value=None, another_key=None):
        databases = [self.cn_db, self.tw_db, self.jp_db]
        for db in databases:
            try:
                with db.atomic():
                    model._meta.database = db
                    if value is None:
                        query = model.get(getattr(model, 'unit_id') == self.unit_id)
                    else:
                        if another_key is None:
                            query = model.get(getattr(model, search_type) == value)
                        else:
                            query = model.get(getattr(model, 'unit_id') == self.unit_id)
                            query = query.get(getattr(model, another_key) == value)
                    return getattr(query, return_type)
            except peewee.DoesNotExist:
                continue
    
    def unit_unique_equipment_search(self, return_type, value):
        return self._search(unit_unique_equipment, 'unit_id', return_type, value, 'equip_slot')

    def unit_rarity_search(self, return_type, value):
        return self._search(unit_rarity, 'unit_id', return_type, value, 'rarity')
    
    def unique_equipment_data_search(self, return_type, value, search_type = 'equipment_id'):
        return self._search(unique_equipment_data, search_type, return_type, value)
    
    def unique_equipment_enhance_rate_search(self, return_type, value, search_type = 'equipment_id'):
        return self._search(unique_equipment_enhance_rate, search_type, return_type, value)

    def promotion_bonus_search(self, return_type, value):
        return self._search(promotion_bonus, 'unit_id', return_type, value, 'promotion_level')
    
    def unit_promotion_status_search(self, return_type, value):
        return self._search(unit_promotion_status, 'unit_id', return_type, value, 'promotion_level')
    
    def chara_story_status_search(self, return_type, value, search_type = 'story_id'):
        return self._search(chara_story_status, search_type, return_type, value)
    
    def unit_promotion_search(self, return_type, value):
        return self._search(unit_promotion, 'unit_id', return_type, value, 'promotion_level')
    
    def equipment_enhance_data_search(self, return_type, value, search_type = 'promotion_level'):
        return self._search(equipment_enhance_data, search_type, return_type, value)
    
    def equipment_promotion_level_search(self, return_type, value, search_type = 'equipment_id'):
        return self._search(equipment_data, search_type, return_type, value)
    
    def equipment_data_search(self, return_type, value, search_type = 'equipment_id'):
        return self._search(equipment_data, search_type, return_type, value)
    
    def skill_action_search(self, return_type, value, search_type = 'action_id'):
        return self._search(skill_action, search_type, return_type, value)
    
    # 装备提升值
    def equipment_enhance_rate_search(self, return_type, value, search_type = 'equipment_id'):
        return self._search(equipment_enhance_rate, search_type, return_type, value)

    def get_unit_equipment_id(self):
        try:
            ueq_1 = self.unit_unique_equipment_search('equip_id', 1)
        except:
            return None
        try:
            ueq_2 = self.unit_unique_equipment_search('equip_id', 2)
            if (ueq_2 % 10 != 2) | (ueq_2 // 10 % 1000 != self.unit_id // 100 % 1000):
                return [ueq_1]
        except:
            return [ueq_1]
        return [ueq_1, ueq_2]

# 角色星级基础值 + 角色星级提升值 * (lvl + rank_lvl)
    def get_unit_rarity(self):
        hp = self.unit_rarity_search('hp', self.star)
        atk = self.unit_rarity_search('atk', self.star)
        magic_str = self.unit_rarity_search('magic_str', self.star)
        def_ = self.unit_rarity_search('def_', self.star)
        magic_def = self.unit_rarity_search('magic_def', self.star)
        physical_critical = self.unit_rarity_search('physical_critical', self.star)
        magic_critical = self.unit_rarity_search('magic_critical', self.star)
        wave_hp_recovery = self.unit_rarity_search('wave_hp_recovery', self.star)
        wave_energy_recovery = self.unit_rarity_search('wave_energy_recovery', self.star)
        dodge = self.unit_rarity_search('dodge', self.star)
        physical_penetrate = self.unit_rarity_search('physical_penetrate', self.star)
        magic_penetrate = self.unit_rarity_search('magic_penetrate', self.star)
        life_steal = self.unit_rarity_search('life_steal', self.star)
        hp_recovery_rate = self.unit_rarity_search('hp_recovery_rate', self.star)
        energy_recovery_rate = self.unit_rarity_search('energy_recovery_rate', self.star)
        energy_reduce_rate = self.unit_rarity_search('energy_reduce_rate', self.star)
        accuracy = self.unit_rarity_search('accuracy', self.star)
        # 打包成字典
        unit_rarity_dict = {
            'hp': hp,
            'atk': atk,
            'magic_str': magic_str,
            'def': def_,
            'magic_def': magic_def,
            'physical_critical': physical_critical,
            'magic_critical': magic_critical,
            'wave_hp_recovery': wave_hp_recovery,
            'wave_energy_recovery': wave_energy_recovery,
            'dodge': dodge,
            'physical_penetrate': physical_penetrate,
            'magic_penetrate': magic_penetrate,
            'life_steal': life_steal,
            'hp_recovery_rate': hp_recovery_rate,
            'energy_recovery_rate': energy_recovery_rate,
            'energy_reduce_rate': energy_reduce_rate,
            'accuracy': accuracy
        }
        hp_growth = self.unit_rarity_search('hp_growth', self.star)
        atk_growth = self.unit_rarity_search('atk_growth', self.star)
        magic_str_growth = self.unit_rarity_search('magic_str_growth', self.star)
        def_growth = self.unit_rarity_search('def_growth', self.star)
        magic_def_growth = self.unit_rarity_search('magic_def_growth', self.star)
        physical_critical_growth = self.unit_rarity_search('physical_critical_growth', self.star)
        magic_critical_growth = self.unit_rarity_search('magic_critical_growth', self.star)
        wave_hp_recovery_growth = self.unit_rarity_search('wave_hp_recovery_growth', self.star)
        wave_energy_recovery_growth = self.unit_rarity_search('wave_energy_recovery_growth', self.star)
        dodge_growth = self.unit_rarity_search('dodge_growth', self.star)
        physical_penetrate_growth = self.unit_rarity_search('physical_penetrate_growth', self.star)
        magic_penetrate_growth = self.unit_rarity_search('magic_penetrate_growth', self.star)
        life_steal_growth = self.unit_rarity_search('life_steal_growth', self.star)
        hp_recovery_rate_growth = self.unit_rarity_search('hp_recovery_rate_growth', self.star)
        energy_recovery_rate_growth = self.unit_rarity_search('energy_recovery_rate_growth', self.star)
        energy_reduce_rate_growth = self.unit_rarity_search('energy_reduce_rate_growth', self.star)
        accuracy_growth = self.unit_rarity_search('accuracy_growth', self.star)
        # 打包成字典
        unit_rarity_growth_dict = {
            'hp_growth': hp_growth,
            'atk_growth': atk_growth,
            'magic_str_growth': magic_str_growth,
            'def_growth': def_growth,
            'magic_def_growth': magic_def_growth,
            'physical_critical_growth': physical_critical_growth,
            'magic_critical_growth': magic_critical_growth,
            'wave_hp_recovery_growth': wave_hp_recovery_growth,
            'wave_energy_recovery_growth': wave_energy_recovery_growth,
            'dodge_growth': dodge_growth,
            'physical_penetrate_growth': physical_penetrate_growth,
            'magic_penetrate_growth': magic_penetrate_growth,
            'life_steal_growth': life_steal_growth,
            'hp_recovery_rate_growth': hp_recovery_rate_growth,
            'energy_recovery_rate_growth': energy_recovery_rate_growth,
            'energy_reduce_rate_growth': energy_reduce_rate_growth,
            'accuracy_growth': accuracy_growth
        }
        return unit_rarity_dict, unit_rarity_growth_dict

# 角色专武基础值
    def get_unique_equipment_data(self):
        equipment_id_list = self.get_unit_equipment_id()
        if equipment_id_list is None:
            return None
        unique_equipment_data_list = []
        for equipment_id in equipment_id_list:
            hp = self.unique_equipment_data_search('hp', equipment_id)
            atk = self.unique_equipment_data_search('atk', equipment_id)
            magic_str = self.unique_equipment_data_search('magic_str', equipment_id)
            def_ = self.unique_equipment_data_search('def_', equipment_id)
            magic_def = self.unique_equipment_data_search('magic_def', equipment_id)
            physical_critical = self.unique_equipment_data_search('physical_critical', equipment_id)
            magic_critical = self.unique_equipment_data_search('magic_critical', equipment_id)
            wave_hp_recovery = self.unique_equipment_data_search('wave_hp_recovery', equipment_id)
            wave_energy_recovery = self.unique_equipment_data_search('wave_energy_recovery', equipment_id)
            dodge = self.unique_equipment_data_search('dodge', equipment_id)
            physical_penetrate = self.unique_equipment_data_search('physical_penetrate', equipment_id)
            magic_penetrate = self.unique_equipment_data_search('magic_penetrate', equipment_id)
            life_steal = self.unique_equipment_data_search('life_steal', equipment_id)
            hp_recovery_rate = self.unique_equipment_data_search('hp_recovery_rate', equipment_id)
            energy_recovery_rate = self.unique_equipment_data_search('energy_recovery_rate', equipment_id)
            energy_reduce_rate = self.unique_equipment_data_search('energy_reduce_rate', equipment_id)
            accuracy = self.unique_equipment_data_search('accuracy', equipment_id)
            # 打包成字典
            unique_equipment_data_dict = {
                'equipment_id': equipment_id,
                'hp': hp,
                'atk': atk,
                'magic_str': magic_str,
                'def': def_,
                'magic_def': magic_def,
                'physical_critical': physical_critical,
                'magic_critical': magic_critical,
                'wave_hp_recovery': wave_hp_recovery,
                'wave_energy_recovery': wave_energy_recovery,
                'dodge': dodge,
                'physical_penetrate': physical_penetrate,
                'magic_penetrate': magic_penetrate,
                'life_steal': life_steal,
                'hp_recovery_rate': hp_recovery_rate,
                'energy_recovery_rate': energy_recovery_rate,
                'energy_reduce_rate': energy_reduce_rate,
                'accuracy': accuracy
            }
            unique_equipment_data_list.append(unique_equipment_data_dict)
        return unique_equipment_data_list

# 角色专武提升值 * (lvl - 1)
    def get_unique_equipment_enhance_rate(self):
        equipment_id_list = self.get_unit_equipment_id()
        unique_equipment_enhance_rate_list = []
        for equipment_id in equipment_id_list:
            hp = self.unique_equipment_enhance_rate_search('hp', equipment_id)
            atk = self.unique_equipment_enhance_rate_search('atk', equipment_id)
            magic_str = self.unique_equipment_enhance_rate_search('magic_str', equipment_id)
            def_ = self.unique_equipment_enhance_rate_search('def_', equipment_id)
            magic_def = self.unique_equipment_enhance_rate_search('magic_def', equipment_id)
            physical_critical = self.unique_equipment_enhance_rate_search('physical_critical', equipment_id)
            magic_critical = self.unique_equipment_enhance_rate_search('magic_critical', equipment_id)
            wave_hp_recovery = self.unique_equipment_enhance_rate_search('wave_hp_recovery', equipment_id)
            wave_energy_recovery = self.unique_equipment_enhance_rate_search('wave_energy_recovery', equipment_id)
            dodge = self.unique_equipment_enhance_rate_search('dodge', equipment_id)
            physical_penetrate = self.unique_equipment_enhance_rate_search('physical_penetrate', equipment_id)
            magic_penetrate = self.unique_equipment_enhance_rate_search('magic_penetrate', equipment_id)
            life_steal = self.unique_equipment_enhance_rate_search('life_steal', equipment_id)
            hp_recovery_rate = self.unique_equipment_enhance_rate_search('hp_recovery_rate', equipment_id)
            energy_recovery_rate = self.unique_equipment_enhance_rate_search('energy_recovery_rate', equipment_id)
            energy_reduce_rate = self.unique_equipment_enhance_rate_search('energy_reduce_rate', equipment_id)
            accuracy = self.unique_equipment_enhance_rate_search('accuracy', equipment_id)
            # 打包成字典
            unique_equipment_enhance_rate_dict = {
                'equipment_id': equipment_id,
                'hp': hp,
                'atk': atk,
                'magic_str': magic_str,
                'def': def_,
                'magic_def': magic_def,
                'physical_critical': physical_critical,
                'magic_critical': magic_critical,
                'wave_hp_recovery': wave_hp_recovery,
                'wave_energy_recovery': wave_energy_recovery,
                'dodge': dodge,
                'physical_penetrate': physical_penetrate,
                'magic_penetrate': magic_penetrate,
                'life_steal': life_steal,
                'hp_recovery_rate': hp_recovery_rate,
                'energy_recovery_rate': energy_recovery_rate,
                'energy_reduce_rate': energy_reduce_rate,
                'accuracy': accuracy
            }
            unique_equipment_enhance_rate_list.append(unique_equipment_enhance_rate_dict)
        return unique_equipment_enhance_rate_list

# 角色rb提升值
    def get_promotion_bonus(self):
        hp = self.promotion_bonus_search('hp', self.rank)
        if hp is None:
            return None
        atk = self.promotion_bonus_search('atk', self.rank)
        magic_str = self.promotion_bonus_search('magic_str', self.rank)
        def_ = self.promotion_bonus_search('def_', self.rank)
        magic_def = self.promotion_bonus_search('magic_def', self.rank)
        physical_critical = self.promotion_bonus_search('physical_critical', self.rank)
        magic_critical = self.promotion_bonus_search('magic_critical', self.rank)
        wave_hp_recovery = self.promotion_bonus_search('wave_hp_recovery', self.rank)
        wave_energy_recovery = self.promotion_bonus_search('wave_energy_recovery', self.rank)
        dodge = self.promotion_bonus_search('dodge', self.rank)
        physical_penetrate = self.promotion_bonus_search('physical_penetrate', self.rank)
        magic_penetrate = self.promotion_bonus_search('magic_penetrate', self.rank)
        life_steal = self.promotion_bonus_search('life_steal', self.rank)
        hp_recovery_rate = self.promotion_bonus_search('hp_recovery_rate', self.rank)
        energy_recovery_rate = self.promotion_bonus_search('energy_recovery_rate', self.rank)
        energy_reduce_rate = self.promotion_bonus_search('energy_reduce_rate', self.rank)
        accuracy = self.promotion_bonus_search('accuracy', self.rank)
        # 打包成字典
        promotion_bonus_dict = {
            'hp': hp,
            'atk': atk,
            'magic_str': magic_str,
            'def': def_,
            'magic_def': magic_def,
            'physical_critical': physical_critical,
            'magic_critical': magic_critical,
            'wave_hp_recovery': wave_hp_recovery,
            'wave_energy_recovery': wave_energy_recovery,
            'dodge': dodge,
            'physical_penetrate': physical_penetrate,
            'magic_penetrate': magic_penetrate,
            'life_steal': life_steal,
            'hp_recovery_rate': hp_recovery_rate,
            'energy_recovery_rate': energy_recovery_rate,
            'energy_reduce_rate': energy_reduce_rate,
            'accuracy': accuracy
        }
        return promotion_bonus_dict

# 角色rank提升值
    def get_unit_promotion_status(self):
        hp = self.unit_promotion_status_search('hp', self.rank)
        atk = self.unit_promotion_status_search('atk', self.rank)
        magic_str = self.unit_promotion_status_search('magic_str', self.rank)
        def_ = self.unit_promotion_status_search('def_', self.rank)
        magic_def = self.unit_promotion_status_search('magic_def', self.rank)
        physical_critical = self.unit_promotion_status_search('physical_critical', self.rank)
        magic_critical = self.unit_promotion_status_search('magic_critical', self.rank)
        wave_hp_recovery = self.unit_promotion_status_search('wave_hp_recovery', self.rank)
        wave_energy_recovery = self.unit_promotion_status_search('wave_energy_recovery', self.rank)
        dodge = self.unit_promotion_status_search('dodge', self.rank)
        physical_penetrate = self.unit_promotion_status_search('physical_penetrate', self.rank)
        magic_penetrate = self.unit_promotion_status_search('magic_penetrate', self.rank)
        life_steal = self.unit_promotion_status_search('life_steal', self.rank)
        hp_recovery_rate = self.unit_promotion_status_search('hp_recovery_rate', self.rank)
        energy_recovery_rate = self.unit_promotion_status_search('energy_recovery_rate', self.rank)
        energy_reduce_rate = self.unit_promotion_status_search('energy_reduce_rate', self.rank)
        accuracy = self.unit_promotion_status_search('accuracy', self.rank)
        # 打包成字典
        unit_promotion_status_dict = {
            'hp': hp,
            'atk': atk,
            'magic_str': magic_str,
            'def': def_,
            'magic_def': magic_def,
            'physical_critical': physical_critical,
            'magic_critical': magic_critical,
            'wave_hp_recovery': wave_hp_recovery,
            'wave_energy_recovery': wave_energy_recovery,
            'dodge': dodge,
            'physical_penetrate': physical_penetrate,
            'magic_penetrate': magic_penetrate,
            'life_steal': life_steal,
            'hp_recovery_rate': hp_recovery_rate,
            'energy_recovery_rate': energy_recovery_rate,
            'energy_reduce_rate': energy_reduce_rate,
            'accuracy': accuracy
        }
        return unit_promotion_status_dict

# 角色好感提升值
    def get_chara_story_status(self):
        story_chara_id_list = []
        status_dict_list = []
        for i in range(1, 11):
            story_chara_id = self.chara_story_status_search(f'chara_id_{i}', (self.unit_id - 1) * 10 + 2)
            if story_chara_id:
                story_chara_id_list.append(story_chara_id)
            else:
                break
        for story_chara_id in story_chara_id_list:
            story_arr = 2
            chara_status_dict = {}
            while story_arr < 13:
                status_type_list = []
                status_rate_list = []
                for i in range(1, 6):
                    status_type = self.chara_story_status_search(f'status_type_{i}', story_chara_id * 1000 + story_arr)
                    if status_type:
                        status_type_list.append(status_type)
                        status_rate = self.chara_story_status_search(f'status_rate_{i}', story_chara_id * 1000 + story_arr)
                        status_rate_list.append(status_rate)
                    else:
                        break
                chara_story_status_dict = {
                    'chara_id': story_chara_id,
                    'status_type': status_type_list,
                    'status_rate': status_rate_list
                }
                if chara_story_status_dict['status_type'] == []:
                    break
                chara_status_dict[story_chara_id * 1000 + story_arr] = chara_story_status_dict
                story_arr += 1
            status_dict_list.append(chara_status_dict)
        return status_dict_list
# 结构梳理
# 数组里面存放这个角色不同换皮的数据字典
# 数据字典里面存放了这个换皮每级好感的数值字典
# 这个字典包含了换皮id(chara_id)，提升类型(status_type)和提升数值(status_rate)


# 角色装备位置
# 1左上 2右上 3左中 4右中 5左下 6右下
    def get_unit_promotion(self):
        equip_slot_list = []
        for i in range(1, 7):
            equip_slot = self.unit_promotion_search(f'equip_slot_{i}', self.rank)
            equip_slot_list.append(equip_slot)
        return equip_slot_list

# 装备品质查询
    def get_equipment_promotion_level(self, equipment_id):
        promotion_level = self.equipment_promotion_level_search('promotion_level', equipment_id)
        return promotion_level

# 装备升级次数
    def get_equipment_enhance_data(self, promotion_level):
        equipment_enhance_level = max(self.equipment_enhance_data_search('equipment_enhance_level', promotion_level))
        return equipment_enhance_level
    
# 角色装备值
    def get_equipment_value(self, equip_level):
        equip_list = self.get_unit_promotion()
        equipment_value_list = []
        i = 0
        for equip in equip_list:
            if equip == 999999:
                continue
            equip_promotion_level = self.get_equipment_promotion_level(equip)
            if equip_level[i] > equip_promotion_level:
                return 'lvl_error'
            hp = self.equipment_data_search('hp', equip)
            atk = self.equipment_data_search('atk', equip)
            magic_str = self.equipment_data_search('magic_str', equip)
            def_ = self.equipment_data_search('def_', equip)
            magic_def = self.equipment_data_search('magic_def', equip)
            physical_critical = self.equipment_data_search('physical_critical', equip)
            magic_critical = self.equipment_data_search('magic_critical', equip)
            wave_hp_recovery = self.equipment_data_search('wave_hp_recovery', equip)
            wave_energy_recovery = self.equipment_data_search('wave_energy_recovery', equip)
            dodge = self.equipment_data_search('dodge', equip)
            physical_penetrate = self.equipment_data_search('physical_penetrate', equip)
            magic_penetrate = self.equipment_data_search('magic_penetrate', equip)
            life_steal = self.equipment_data_search('life_steal', equip)
            hp_recovery_rate = self.equipment_data_search('hp_recovery_rate', equip)
            energy_recovery_rate = self.equipment_data_search('energy_recovery_rate', equip)
            energy_reduce_rate = self.equipment_data_search('energy_reduce_rate', equip)
            accuracy = self.equipment_data_search('accuracy', equip)
            # 根据装备星级计算数值
            if equip_level[i] != 0:
                hp += self.equipment_enhance_rate_search('hp', equip) * equip_level[i]
                atk += self.equipment_enhance_rate_search('atk', equip) * equip_level[i]
                magic_str += self.equipment_enhance_rate_search('magic_str', equip) * equip_level[i]
                def_ += self.equipment_enhance_rate_search('def_', equip) * equip_level[i]
                magic_def += self.equipment_enhance_rate_search('magic_def', equip) * equip_level[i]
                physical_critical += self.equipment_enhance_rate_search('physical_critical', equip) * equip_level[i]
                magic_critical += self.equipment_enhance_rate_search('magic_critical', equip) * equip_level[i]
                wave_hp_recovery += self.equipment_enhance_rate_search('wave_hp_recovery', equip) * equip_level[i]
                wave_energy_recovery += self.equipment_enhance_rate_search('wave_energy_recovery', equip) * equip_level[i]
                dodge += self.equipment_enhance_rate_search('dodge', equip) * equip_level[i]
                physical_penetrate += self.equipment_enhance_rate_search('physical_penetrate', equip) * equip_level[i]
                magic_penetrate += self.equipment_enhance_rate_search('magic_penetrate', equip) * equip_level[i]
                life_steal += self.equipment_enhance_rate_search('life_steal', equip) * equip_level[i]
                hp_recovery_rate += self.equipment_enhance_rate_search('hp_recovery_rate', equip) * equip_level[i]
                energy_recovery_rate += self.equipment_enhance_rate_search('energy_recovery_rate', equip) * equip_level[i]
                energy_reduce_rate += self.equipment_enhance_rate_search('energy_reduce_rate', equip) * equip_level[i]
                accuracy += self.equipment_enhance_rate_search('accuracy', equip) * equip_level[i]
            # 打包成字典
            equipment_value_dict = {
                'equip_slot': equip,
                'hp': hp,
                'atk': atk,
                'magic_str': magic_str,
                'def': def_,
                'magic_def': magic_def,
                'physical_critical': physical_critical,
                'magic_critical': magic_critical,
                'wave_hp_recovery': wave_hp_recovery,
                'wave_energy_recovery': wave_energy_recovery,
                'dodge': dodge,
                'physical_penetrate': physical_penetrate,
                'magic_penetrate': magic_penetrate,
                'life_steal': life_steal,
                'hp_recovery_rate': hp_recovery_rate,
                'energy_recovery_rate': energy_recovery_rate,
                'energy_reduce_rate': energy_reduce_rate,
                'accuracy': accuracy
            }
            i += 1
            equipment_value_list.append(equipment_value_dict)
        return equipment_value_list

# 角色EX提升值
    def get_ex_skill_level(self):
        if self.star  < 5:
            action_id = self.unit_id // 100 * 100000 + 50101
        else:
            action_id = self.unit_id // 100 * 10000 + 51101
        ex_type = self.skill_action_search('action_detail_1', action_id)
        value_1 = self.skill_action_search('action_value_2', action_id)
        value_2 = self.skill_action_search('action_value_3', action_id)
        return [ex_type, value_1, value_2]

# 全数值处理计算
    def calculate_all_value(self):
        list_of_equip = [1, 1, 1, 1, 1, 1]
        unit_rarity_value, unit_rarity_growth = self.get_unit_rarity()
        unique_equipment_data_value = self.get_unique_equipment_data()
        unique_equipment_enhance_rate_value = self.get_unique_equipment_enhance_rate()
        unit_promotion_status_value = self.get_unit_promotion_status()
        promotion_bonus_value = self.get_promotion_bonus()
        chara_story_status_value = self.get_chara_story_status()
        equipment_data_value = self.get_equipment_value(list_of_equip)
        ex_skill_level_value = self.get_ex_skill_level()
        if equipment_data_value == 'lvl_error':
            return '装备等级有误，请检查'
        hp = unit_rarity_value['hp'] + unit_rarity_growth['hp_growth'] * (self.level + self.rank)
        atk = unit_rarity_value['atk'] + unit_rarity_growth['atk_growth'] * (self.level + self.rank)
        magic_str = unit_rarity_value['magic_str'] + unit_rarity_growth['magic_str_growth'] * (self.level + self.rank)
        def_ = unit_rarity_value['def'] + unit_rarity_growth['def_growth'] * (self.level + self.rank)
        magic_def = unit_rarity_value['magic_def'] + unit_rarity_growth['magic_def_growth'] * (self.level + self.rank)
        physical_critical = unit_rarity_value['physical_critical'] + unit_rarity_growth['physical_critical_growth'] * (self.level + self.rank)
        magic_critical = unit_rarity_value['magic_critical'] + unit_rarity_growth['magic_critical_growth'] * (self.level + self.rank)
        wave_hp_recovery = unit_rarity_value['wave_hp_recovery'] + unit_rarity_growth['wave_hp_recovery_growth'] * (self.level + self.rank)
        wave_energy_recovery = unit_rarity_value['wave_energy_recovery'] + unit_rarity_growth['wave_energy_recovery_growth'] * (self.level + self.rank)
        dodge = unit_rarity_value['dodge'] + unit_rarity_growth['dodge_growth'] * (self.level + self.rank)
        physical_penetrate = unit_rarity_value['physical_penetrate'] + unit_rarity_growth['physical_penetrate_growth'] * (self.level + self.rank)
        magic_penetrate = unit_rarity_value['magic_penetrate'] + unit_rarity_growth['magic_penetrate_growth'] * (self.level + self.rank)
        life_steal = unit_rarity_value['life_steal'] + unit_rarity_growth['life_steal_growth'] * (self.level + self.rank)
        hp_recovery_rate = unit_rarity_value['hp_recovery_rate'] + unit_rarity_growth['hp_recovery_rate_growth'] * (self.level + self.rank)
        energy_recovery_rate = unit_rarity_value['energy_recovery_rate'] + unit_rarity_growth['energy_recovery_rate_growth'] * (self.level + self.rank)
        energy_reduce_rate = unit_rarity_value['energy_reduce_rate'] + unit_rarity_growth['energy_reduce_rate_growth'] * (self.level + self.rank)
        accuracy = unit_rarity_value['accuracy'] + unit_rarity_growth['accuracy_growth'] * (self.level + self.rank)
        if self.rank > 1:
            hp += unit_promotion_status_value['hp']
            atk += unit_promotion_status_value['atk']
            magic_str += unit_promotion_status_value['magic_str']
            def_ += unit_promotion_status_value['def']
            magic_def += unit_promotion_status_value['magic_def']
            physical_critical += unit_promotion_status_value['physical_critical']
            magic_critical += unit_promotion_status_value['magic_critical']
            wave_hp_recovery += unit_promotion_status_value['wave_hp_recovery']
            wave_energy_recovery += unit_promotion_status_value['wave_energy_recovery']
            dodge += unit_promotion_status_value['dodge']
            physical_penetrate += unit_promotion_status_value['physical_penetrate']
            magic_penetrate += unit_promotion_status_value['magic_penetrate']
            life_steal += unit_promotion_status_value['life_steal']
            hp_recovery_rate += unit_promotion_status_value['hp_recovery_rate']
            energy_recovery_rate += unit_promotion_status_value['energy_recovery_rate']
            energy_reduce_rate += unit_promotion_status_value['energy_reduce_rate']
            accuracy += unit_promotion_status_value['accuracy']
        for unique_equipment_data_dict, unique_equipment_enhance_rate_dict in zip(unique_equipment_data_value, unique_equipment_enhance_rate_value):
            hp += unique_equipment_data_dict['hp'] + unique_equipment_enhance_rate_dict['hp'] * (self.unique_level - 1)
            atk += unique_equipment_data_dict['atk'] + unique_equipment_enhance_rate_dict['atk'] * (self.unique_level - 1)
            magic_str += unique_equipment_data_dict['magic_str'] + unique_equipment_enhance_rate_dict['magic_str'] * (self.unique_level - 1)
            def_ += unique_equipment_data_dict['def'] + unique_equipment_enhance_rate_dict['def'] * (self.unique_level - 1)
            magic_def += unique_equipment_data_dict['magic_def'] + unique_equipment_enhance_rate_dict['magic_def'] * (self.unique_level - 1)
            physical_critical += unique_equipment_data_dict['physical_critical'] + unique_equipment_enhance_rate_dict['physical_critical'] * (self.unique_level - 1)
            magic_critical += unique_equipment_data_dict['magic_critical'] + unique_equipment_enhance_rate_dict['magic_critical'] * (self.unique_level - 1)
            wave_hp_recovery += unique_equipment_data_dict['wave_hp_recovery'] + unique_equipment_enhance_rate_dict['wave_hp_recovery'] * (self.unique_level - 1)
            wave_energy_recovery += unique_equipment_data_dict['wave_energy_recovery'] + unique_equipment_enhance_rate_dict['wave_energy_recovery'] * (self.unique_level - 1)
            dodge += unique_equipment_data_dict['dodge'] + unique_equipment_enhance_rate_dict['dodge'] * (self.unique_level - 1)
            physical_penetrate += unique_equipment_data_dict['physical_penetrate'] + unique_equipment_enhance_rate_dict['physical_penetrate'] * (self.unique_level - 1)
            magic_penetrate += unique_equipment_data_dict['magic_penetrate'] + unique_equipment_enhance_rate_dict['magic_penetrate'] * (self.unique_level - 1)
            life_steal += unique_equipment_data_dict['life_steal'] + unique_equipment_enhance_rate_dict['life_steal'] * (self.unique_level - 1)
            hp_recovery_rate += unique_equipment_data_dict['hp_recovery_rate'] + unique_equipment_enhance_rate_dict['hp_recovery_rate'] * (self.unique_level - 1)
            energy_recovery_rate += unique_equipment_data_dict['energy_recovery_rate'] + unique_equipment_enhance_rate_dict['energy_recovery_rate'] * (self.unique_level - 1)
            energy_reduce_rate += unique_equipment_data_dict['energy_reduce_rate'] + unique_equipment_enhance_rate_dict['energy_reduce_rate'] * (self.unique_level - 1)
            accuracy += unique_equipment_data_dict['accuracy'] + unique_equipment_enhance_rate_dict['accuracy'] * (self.unique_level - 1)
        if promotion_bonus_value is not None:
            hp += promotion_bonus_value['hp']
            atk += promotion_bonus_value['atk']
            magic_str += promotion_bonus_value['magic_str']
            def_ += promotion_bonus_value['def']
            magic_def += promotion_bonus_value['magic_def']
            physical_critical += promotion_bonus_value['physical_critical']
            magic_critical += promotion_bonus_value['magic_critical']
            wave_hp_recovery += promotion_bonus_value['wave_hp_recovery']
            wave_energy_recovery += promotion_bonus_value['wave_energy_recovery']
            dodge += promotion_bonus_value['dodge']
            physical_penetrate += promotion_bonus_value['physical_penetrate']
            magic_penetrate += promotion_bonus_value['magic_penetrate']
            life_steal += promotion_bonus_value['life_steal']
            hp_recovery_rate += promotion_bonus_value['hp_recovery_rate']
            energy_recovery_rate += promotion_bonus_value['energy_recovery_rate']
            energy_reduce_rate += promotion_bonus_value['energy_reduce_rate']
            accuracy += promotion_bonus_value['accuracy']
        story_hp = 0
        story_atk = 0
        story_def = 0
        story_magic_str = 0
        story_magic_def = 0
        story_physical_critical = 0
        story_magic_critical = 0
        story_dodge = 0
        story_life_steal = 0
        story_wave_hp_recovery = 0
        story_wave_energy_recovery = 0
        story_energy_recovery_rate = 0
        story_hp_recovery_rate = 0
        story_accuracy = 0
        for chara_story_status_dict in chara_story_status_value:
            for story_status_dict in chara_story_status_dict.values():
                for status_type, status_rate in zip(story_status_dict['status_type'], story_status_dict['status_rate']):
                    if status_type == 1:
                        story_hp += status_rate
                    elif status_type == 2:
                        story_atk += status_rate
                    elif status_type == 3:
                        story_def += status_rate
                    elif status_type == 4:
                        story_magic_str += status_rate
                    elif status_type == 5:
                        story_magic_def += status_rate
                    elif status_type == 6:
                        story_physical_critical += status_rate
                    elif status_type == 7:
                        story_magic_critical += status_rate
                    elif status_type == 8:
                        story_dodge += status_rate
                    elif status_type == 9:
                        story_life_steal += status_rate
                    elif status_type == 10:
                        story_wave_hp_recovery += status_rate
                    elif status_type == 11:
                        story_wave_energy_recovery += status_rate
                    elif status_type == 14:
                        story_energy_recovery_rate += status_rate
                    elif status_type == 15:
                        story_hp_recovery_rate += status_rate
                    elif status_type == 17:
                        story_accuracy += status_rate
        hp += story_hp
        atk += story_atk
        def_ += story_def
        magic_str += story_magic_str
        magic_def += story_magic_def
        physical_critical += story_physical_critical
        magic_critical += story_magic_critical
        dodge += story_dodge
        life_steal += story_life_steal
        wave_hp_recovery += story_wave_hp_recovery
        wave_energy_recovery += story_wave_energy_recovery
        energy_recovery_rate += story_energy_recovery_rate
        hp_recovery_rate += story_hp_recovery_rate
        accuracy += story_accuracy
        for equipment_data_dict in equipment_data_value:
            hp += equipment_data_dict['hp']
            atk += equipment_data_dict['atk']
            magic_str += equipment_data_dict['magic_str']
            def_ += equipment_data_dict['def']
            magic_def += equipment_data_dict['magic_def']
            physical_critical += equipment_data_dict['physical_critical']
            magic_critical += equipment_data_dict['magic_critical']
            wave_hp_recovery += equipment_data_dict['wave_hp_recovery']
            wave_energy_recovery += equipment_data_dict['wave_energy_recovery']
            dodge += equipment_data_dict['dodge']
            physical_penetrate += equipment_data_dict['physical_penetrate']
            magic_penetrate += equipment_data_dict['magic_penetrate']
            life_steal += equipment_data_dict['life_steal']
            hp_recovery_rate += equipment_data_dict['hp_recovery_rate']
            energy_recovery_rate += equipment_data_dict['energy_recovery_rate']
            energy_reduce_rate += equipment_data_dict['energy_reduce_rate']
            accuracy += equipment_data_dict['accuracy']
        if ex_skill_level_value[0] == 1:
            hp += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 2:
            atk += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 3:
            def_ += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 4:
            magic_str += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 5:
            magic_def += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 6:
            physical_critical += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        elif ex_skill_level_value[0] == 7:
            magic_critical += ex_skill_level_value[1] + ex_skill_level_value[2] * self.ex_level
        else:
            return f'EX技能类型错误，角色ID：{self.unit_id}。请至github反馈'
        # 属性转义中文输出
        result = ''
        result += f'HP: {hp}\n'
        result += f'物理攻击力: {atk}\n'
        result += f'物理防御力: {def_}\n'
        result += f'魔法攻击力: {magic_str}\n'
        result += f'魔法防御力: {magic_def}\n'
        result += f'物理暴击: {physical_critical}\n'
        result += f'魔法暴击: {magic_critical}\n'
        result += f'物理穿透: {physical_penetrate}\n'
        result += f'魔法穿透: {magic_penetrate}\n'
        result += f'回避: {dodge}\n'
        result += f'HP吸收: {life_steal}\n'
        result += f'HP回复: {wave_hp_recovery}\n'
        result += f'TP回复: {wave_energy_recovery}\n'
        result += f'TP上升: {energy_recovery_rate}\n'
        result += f'回复上升: {hp_recovery_rate}\n'
        result += f'命中: {accuracy}\n'
        result += f'TP减少: {energy_reduce_rate}\n'
        result += '=============================\n'
        result += '其中剧情属性：\n'
        if story_hp > 0:
            result += f'HP: {story_hp}\n'
        if story_atk > 0:
            result += f'物理攻击力: {story_atk}\n'
        if story_def > 0:
            result += f'物理防御力: {story_def}\n'
        if story_magic_str > 0:
            result += f'魔法攻击力: {story_magic_str}\n'
        if story_magic_def > 0:
            result += f'魔法防御力: {story_magic_def}\n'
        if story_physical_critical > 0:
            result += f'物理暴击: {story_physical_critical}\n'
        if story_magic_critical > 0:
            result += f'魔法暴击: {story_magic_critical}\n'
        if story_dodge > 0:
            result += f'回避: {story_dodge}\n'
        if story_life_steal > 0:
            result += f'HP吸收: {story_life_steal}\n'
        if story_wave_hp_recovery > 0:
            result += f'HP回复: {story_wave_hp_recovery}\n'
        if story_wave_energy_recovery > 0:
            result += f'TP回复: {story_wave_energy_recovery}\n'
        if story_energy_recovery_rate > 0:
            result += f'TP上升: {story_energy_recovery_rate}\n'
        if story_hp_recovery_rate > 0:
            result += f'回复上升: {story_hp_recovery_rate}\n'
        if story_accuracy > 0:
            result += f'命中: {story_accuracy}\n'
        result += '=============================\n'
        result += '角色星级：\n'
        result += f'{self.star}\n'
        result += '专武等级：\n'
        result += f'{self.unique_level}\n'
        result += 'EX技能等级：\n'
        result += f'{self.ex_level}\n'
        return result


# 计算方法为：角色星级基础值 + 角色星级提升值 * (lvl + rank_lvl) + 角色专武基础值 + 角色专武提升值 * (lvl - 1) + 角色rank提升值 + 角色rb提升值 + 
#            角色好感提升值 + 角色装备基础值 + 角色装备提升值 + 角色ex技能提升值
# 角色好感提升type:
# 1 HP 
# 2 ATK 物理攻击力
# 3 DEF 物理防御力
# 4 MAGIC_STR 魔法攻击力
# 5 MAGIC_DEF 魔法防御力
# 6 PHYSICAL_CRITICAL 物理暴击
# 7 MAGIC_CRITICAL 魔法暴击
# 8 DODGE 回避
# 9 LIFE_STEAL 吸血
# 10 WAVE_HP_RECOVERY HP回复
# 11 WAVE_ENERGY_RECOVERY TP回复
# 14 ENERGY_RECOVERY_RATE TP上升
# 15 HP_RECOVERY_RATE 回复上升
# 17 ACCURACY 命中

class BaseModel(peewee.Model):
    class Meta:
        database = None

# rank bonus 数值
class promotion_bonus(BaseModel):
    unit_id = peewee.IntegerField()
    promotion_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    accuracy = peewee.FloatField()
    class Meta:
        primary_key = peewee.CompositeKey('unit_id', 'promotion_level')

# 角色星级数值
class unit_rarity(BaseModel):
    unit_id = peewee.IntegerField()
    rarity = peewee.IntegerField()
    hp = peewee.FloatField()
    hp_growth = peewee.FloatField()
    atk = peewee.FloatField() 
    atk_growth = peewee.FloatField()
    magic_str = peewee.FloatField()
    magic_str_growth = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    def_growth = peewee.FloatField()
    magic_def = peewee.FloatField()
    magic_def_growth = peewee.FloatField()
    physical_critical = peewee.FloatField()
    physical_critical_growth = peewee.FloatField()
    magic_critical = peewee.FloatField()
    magic_critical_growth = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_hp_recovery_growth = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    wave_energy_recovery_growth = peewee.FloatField()
    dodge = peewee.FloatField()
    dodge_growth = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    physical_penetrate_growth = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    magic_penetrate_growth = peewee.FloatField()
    life_steal = peewee.FloatField()
    life_steal_growth = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    hp_recovery_rate_growth = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_recovery_rate_growth = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    energy_reduce_rate_growth = peewee.FloatField()
    unit_material_id = peewee.IntegerField()
    consume_num = peewee.IntegerField()
    consume_gold = peewee.IntegerField()
    accuracy = peewee.FloatField()
    accuracy_growth = peewee.FloatField()
    class Meta:
        primary_key = peewee.CompositeKey('unit_id', 'rarity')

# 角色专武基础值
class unique_equipment_data(BaseModel):
    equipment_id = peewee.IntegerField(primary_key=True)
    equipment_name = peewee.TextField()
    description = peewee.TextField()
    promotion_level = peewee.IntegerField()
    craft_flg = peewee.IntegerField()
    equipment_enhance_point = peewee.IntegerField() 
    sale_price = peewee.IntegerField()
    require_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    enable_donation = peewee.IntegerField()
    accuracy = peewee.FloatField()

# 角色专武提示数值
class unique_equipment_enhance_rate(BaseModel):
    equipment_id = peewee.IntegerField(primary_key=True)
    equipment_name = peewee.TextField()
    description = peewee.TextField()
    promotion_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    accuracy = peewee.FloatField()

# 角色rank提升值
class unit_promotion_status(BaseModel):
    unit_id = peewee.IntegerField()
    promotion_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    accuracy = peewee.FloatField()
    class Meta:
        primary_key = peewee.CompositeKey('unit_id', 'promotion_level')

# 角色装备基础值
class equipment_data(BaseModel):
    equipment_id = peewee.IntegerField(primary_key=True)
    equipment_name = peewee.TextField()
    description = peewee.TextField()
    original_equipment_id = peewee.IntegerField()
    promotion_level = peewee.IntegerField()
    equipment_type = peewee.IntegerField()
    equipment_category = peewee.IntegerField()
    craft_flg = peewee.IntegerField()
    equipment_enhance_point = peewee.IntegerField()
    sale_price = peewee.IntegerField()
    require_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    enable_donation = peewee.IntegerField()
    accuracy = peewee.FloatField()
    display_item = peewee.IntegerField()
    item_type = peewee.IntegerField()

# 角色装备提升值
class equipment_enhance_rate(BaseModel):
    equipment_id = peewee.IntegerField(primary_key=True)
    equipment_name = peewee.TextField()
    description = peewee.TextField()
    promotion_level = peewee.IntegerField()
    hp = peewee.FloatField()
    atk = peewee.FloatField()
    magic_str = peewee.FloatField()
    def_ = peewee.FloatField(column_name='def')
    magic_def = peewee.FloatField()
    physical_critical = peewee.FloatField()
    magic_critical = peewee.FloatField()
    wave_hp_recovery = peewee.FloatField()
    wave_energy_recovery = peewee.FloatField()
    dodge = peewee.FloatField()
    physical_penetrate = peewee.FloatField()
    magic_penetrate = peewee.FloatField()
    life_steal = peewee.FloatField()
    hp_recovery_rate = peewee.FloatField()
    energy_recovery_rate = peewee.FloatField()
    energy_reduce_rate = peewee.FloatField()
    accuracy = peewee.FloatField()

# 角色专武对照表
class unit_unique_equipment(BaseModel):
    unit_id = peewee.IntegerField()
    equip_slot = peewee.IntegerField()
    equip_id = peewee.IntegerField()
    class Meta:
        primary_key = peewee.CompositeKey('unit_id', 'equip_slot')

# 角色好感提升值
class chara_story_status(BaseModel):
    story_id = peewee.IntegerField()
    unlock_story_name = peewee.TextField()
    status_type_1 = peewee.IntegerField()
    status_rate_1 = peewee.IntegerField()
    status_type_2 = peewee.IntegerField()
    status_rate_2 = peewee.IntegerField()
    status_type_3 = peewee.IntegerField()
    status_rate_3 = peewee.IntegerField()
    status_type_4 = peewee.IntegerField()
    status_rate_4 = peewee.IntegerField()
    status_type_5 = peewee.IntegerField()
    status_rate_5 = peewee.IntegerField()
    chara_id_1 = peewee.IntegerField()
    chara_id_2 = peewee.IntegerField()
    chara_id_3 = peewee.IntegerField()
    chara_id_4 = peewee.IntegerField()
    chara_id_5 = peewee.IntegerField()
    chara_id_6 = peewee.IntegerField()
    chara_id_7 = peewee.IntegerField()
    chara_id_8 = peewee.IntegerField()
    chara_id_9 = peewee.IntegerField()
    chara_id_10 = peewee.IntegerField()
    chara_id_11 = peewee.IntegerField()
    chara_id_12 = peewee.IntegerField()
    chara_id_13 = peewee.IntegerField()
    chara_id_14 = peewee.IntegerField()
    chara_id_15 = peewee.IntegerField()
    chara_id_16 = peewee.IntegerField()
    chara_id_17 = peewee.IntegerField()
    chara_id_18 = peewee.IntegerField()
    chara_id_19 = peewee.IntegerField()
    chara_id_20 = peewee.IntegerField()
    class Meta:
        primary_key = peewee.CompositeKey('story_id')

# 角色装备表
class unit_promotion(BaseModel):
    unit_id = peewee.IntegerField()
    promotion_level = peewee.IntegerField()
    equip_slot_1 = peewee.IntegerField()
    equip_slot_2 = peewee.IntegerField()
    equip_slot_3 = peewee.IntegerField()
    equip_slot_4 = peewee.IntegerField()
    equip_slot_5 = peewee.IntegerField()
    equip_slot_6 = peewee.IntegerField()
    class Meta:
        primary_key = peewee.CompositeKey('unit_id', 'promotion_level')

# 装备升级表
class equipment_enhance_data(BaseModel):
    promotion_level = peewee.IntegerField()
    equipment_enhance_level = peewee.IntegerField()
    needed_point = peewee.IntegerField()
    total_point = peewee.IntegerField()
    class Meta:
        primary_key = peewee.CompositeKey('promotion_level', 'equipment_enhance_level')

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
    description = peewee.TextField()
    level_up_disp = peewee.TextField()

if __name__ == '__main__':
    import os
    
    script_path = os.path.dirname(os.path.abspath(__file__))
    cn_db_path = os.path.join(script_path,'redive_cn.db')
    tw_db_path = os.path.join(script_path,'redive_tw.db')
    jp_db_path = os.path.join(script_path,'redive_jp.db')

    cn_db = peewee.SqliteDatabase(cn_db_path)
    tw_db = peewee.SqliteDatabase(tw_db_path)
    jp_db = peewee.SqliteDatabase(jp_db_path)

    c = chara_calculator(100101, 2, 1, 1, 1, 1, cn_db, tw_db, jp_db)
    # print(c.get_unit_rarity())
    # print(c.get_unique_equipment_data())
    # print(c.get_unique_equipment_enhance_rate())
    # print(c.get_unit_promotion_status())
    # print(c.get_promotion_bonus())
    # print(c.get_chara_story_status())
    # print(c.get_equipment_value([1, 1, 1, 1, 1, 1]))
    # print(c.get_ex_skill_level())
    # print(c.get_unit_promotion())
    print(c.calculate_all_value())

