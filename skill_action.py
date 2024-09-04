class SkillAction:
    def __init__(self, action_id, detail1, detail2, detail3, value1, value2, value3, value4, value5, value6, value7, 
                 target_assignment, target_area, target_range, target_type, target_number, target_count, description, level_up_disp,
                 lvl, atk):
        self.id = action_id
        self.detail1 = detail1
        self.detail2 = detail2
        self.detail3 = detail3
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4
        self.value5 = value5
        self.value6 = value6
        self.value7 = value7
        self.target_assignment = target_assignment
        self.target_area = target_area
        self.target_range = target_range
        self.target_type = target_type
        self.target_number = target_number
        self.target_count = target_count
        self.description = description
        self.level_up_disp = level_up_disp
        self.lvl = lvl
        self.atk = atk
        
    def Damage(self):
        result = '对'
        if self.target_number > 0:
            result += f'(第{self.target_number}近)'
        result += '的'
        if self.target_assignment == 1:
            result += '敌方'
        elif self.target_assignment == 2:
            result += '己方'
        else:
            result += '未知目标'
        result += '造成'
        damage = self.value1 + self.value2 * self.lvl + self.value3 * self.atk
        result += f'{self.value1}点'
        if self.detail1 == 1:   # 1: 物理伤害
            pass
        elif self.detail1 == 2: # 2: 魔法伤害
            pass
        elif self.detail1 == 3: # 3: 必中物理伤害
            pass
        elif self.detail1 == 4: # 4: 必中魔法伤害
            pass
        elif self.detail1 == 5: # 5: 总物理伤害
            pass
        elif self.detail1 == 6: # 6: 总魔法伤害
            pass
        else:   # 7: 未知
            pass

    def Move(self):
        pass

    def Ex(self):
        result = '自身的'
        if self.detail1 == 1:   # 1: HP
            result += '生命值'
        elif self.detail1 == 2: # 2: ATK
            result += '物理攻击力'
        elif self.detail1 == 3: # 3: DEF
            result += '物理防御力'
        elif self.detail1 == 4: # 4: MAG_ATK
            result += '魔法攻击力'
        elif self.detail1 == 5: # 5: MAG_DEF
            result += '魔法防御力'
        elif self.detail1 == 6: # 6: PHY_CRIT
            result += '物理暴击率'
        elif self.detail1 == 7: # 7: MAG_CRIT
            result += '魔法暴击率'
        else:   # 8: 未知
            result = '未知属性, 请至github反馈'
            return result
        result += '提升'
        count = self.value2 + self.value3 * self.lvl
        result += f'[{count}]<{self.value2} + {self.value3} * 技能等级>'

    def action_type(self, action_type):
        if action_type == 1:     # 1: 造成伤害
            self.Damage(self)
        elif action_type == 2:   # 2: 位移
            self.Move(self)
        elif action_type == 3:   # 3: 改变对方位置
            pass
        elif action_type == 4:   # 4: 回复HP
            pass
        elif action_type == 6:   # 6: 护盾类型
            pass