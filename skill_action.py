skill_switch = {
    1:  'Damage',       # 造成伤害
    2:  'Move',         # 位移
    3:  'ChangePos',    # 改变对方位置
    4:  'Heal',         # 回复HP
    6:  'Barrier',      # 护盾类型
    7:  'ChooseEnemy',  # 指定攻击对象
    8:  'Speed',        # 行动速度变更
    9:  'Dot',          # 持续伤害
    10: 'Effect',       # buff/debuff
    28: 'IfSp',         # 特殊条件
    35: 'Seal',         # 标记
    90: 'Ex'            # ex技能
}

class SkillAction:
    def __init__(self, action_id, detail1, detail2, detail3, value1, value2, value3, value4, value5, value6, value7, 
                 target_assignment, target_area, target_range, target_type, target_number, target_count, description, level_up_disp,
                 lvl, atk, mag_atk, depend_id):
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
        self.mag_atk = mag_atk
        self.depend_id = depend_id
        self.error = None
    
    def get_target(self):
        position = ''
        target_count = ''
        range_ = ''
        if self.target_assignment == 1:
            if self.target_number > 0:
                position = f'(第{self.target_number + 1}近)'
            else:
                position = '前方'
            target = '敌方'
        elif self.target_assignment == 2:
            target = '己方'
            if self.target_number > 0:
                position = f'(第{self.target_number}近)'
        elif self.target_assignment == 3:
            target = '双方'
        elif self.target_assignment == 0:
            target = '自身'
        else:
            target = '未知目标'
        if self.target_count == 99 and self.target_range == 2160 and self.value6 == 1 and self.value7 == 0 and self.detail2 == 1:
            target = '双方'
        if self.target_type == 0 or self.target_type == 1 or self.target_type == 3 or self.target_type == 40 or self.target_type == 41:
            target_type = '的'
        elif self.target_type == 2:
            target_type = '随机的'
        elif self.target_type == 5 or self.target_type == 25:
            target_type = 'HP最低的'
        elif self.target_type == 6 or self.target_type == 26:
            target_type = 'HP最高的'
        elif self.target_type == 7:
            target_type = '自身'
        elif self.target_type == 9:
            target_type = '最后方的'
        elif self.target_type == 10:
            target_type = '最前方的'
        elif self.target_type == 11:
            target_type = '范围内的'
        elif self.target_type == 12 or self.target_type == 27 or self.target_type == 37:
            target_type = 'TP最高的'
        elif self.target_type == 13 or self.target_type == 19 or self.target_type == 28:
            target_type = 'TP最低的'
        elif self.target_type == 14 or self.target_type == 29:
            target_type = '物理攻击力最高的'
        elif self.target_type == 15 or self.target_type == 30:
            target_type = '物理攻击力最低的'
        elif self.target_type == 16 or self.target_type == 31:
            target_type = '魔法攻击力最高的'
        elif self.target_type == 17 or self.target_type == 32:
            target_type = '魔法攻击力最低的'
        elif self.target_type == 18:
            target_type = '召唤物'
        elif self.target_type == 20:
            target_type = '物理攻击的'
        elif self.target_type == 21:
            target_type = '魔法攻击的'
        elif self.target_type == 22:
            target_type = '随机的召唤物'
        elif self.target_type == 23:
            target_type = '自身的召唤物'
        elif self.target_type == 24:
            target_type = '领主'
        elif self.target_type == 33:
            target_type = '暗影'
        elif self.target_type == 34:
            target_type = '除自身以外'
        elif self.target_type == 35:
            target_type = '剩余HP最高的'
        elif self.target_type == 36:
            target_type = '剩余HP最低的'
        elif self.target_type == 38:
            target_type = '攻击力最高的'
        elif self.target_type == 39:
            target_type = '攻击力最低的'
        elif self.target_type == 42:
            target_type = '多目标'
        elif self.target_type == 43:
            target_type = '物理攻击力最高(自身除外)的'
        elif self.target_type == 44:
            target_type = '剩余HP最低(自身除外)的'
        elif self.target_type == 45:
            target_type = '物理防御力最低的'
        elif self.target_type == 46:
            target_type = '魔法防御力最低的'
        else:
            target_type = '未知目标类型'
            self.error = f'SkillAction:target_type={self.target_type}'
        if self.target_count != 0 and self.target_count != 1 and self.target_count != 99:
            target_count = f'({self.target_count}名)'
        elif self.target_count == 99:
            target_count = '全体'
        if self.target_range in range(1, 2160):
            range_ = f'范围[{self.target_range}]'
        else:
            range_ = f''
        return target, position, target_type, target_count, range_
    
    def Damage(self):
        result = '对'
        target, position, target_type, target_count, range_ = self.get_target()
        if range_:
            result += range_
            result += '内'
        else:
            if position:
                result += position
        if target_type:
            result += target_type
        result += target_count
        result += target
        result += '造成'
        damage = self.value1 + self.value2 * self.lvl + self.value3 * max(self.atk, self.mag_atk)
        damage = round(damage)
        result += f'[{damage}]<{self.value1} + {self.value2} * 技能等级 + {self.value3} * 攻击力>的'
        if self.detail1 == 1:   # 1: 物理伤害
            result += '物理伤害'
        elif self.detail1 == 2: # 2: 魔法伤害
            result += '魔法伤害'
        elif self.detail1 == 3: # 3: 必中物理伤害
            result += '必定命中的物理伤害'
        elif self.detail1 == 4: # 4: 必中魔法伤害
            result += '必定命中的魔法伤害'  # 悄悄吐槽下，国服我都没见过哪个detail1大于3的
        elif self.detail1 == 5: # 5: 总物理伤害
            result += '伤害'    # 这俩我都不知道是啥，做个标记，遇到就修
            self.error = 'Damage:detail1=5'
        elif self.detail1 == 6: # 6: 总魔法伤害
            result += '伤害'
            self.error = 'Damage:detail1=6'
        else:   # 7: 未知
            result = '未知伤害类型, 请至github反馈'
        if self.depend_id:
            result += f'存在受到影响的动作，ID:{self.depend_id}，此消息为bug，请至github反馈'
        return result

    def Move(self):
        result = ''
        return result
    
    def ChangePos(self):
        result = ''
        depend = ''
        if self.depend_id > 0:
            depend = f'受到动作({self.depend_id % 100})影响的'
        if self.detail1 == 1 or self.detail1 == 9:   #击飞敌人
            result += f'击飞{depend}敌方，高度[{round(self.value1)}]'
        elif self.detail1 == 3 or self.detail1 == 6:   #击退敌人
            result += f'击退{depend}敌方，距离[{abs(round(self.value1))}]'
        elif self.detail1 == 8:   # 拉近敌人
            result += f'将{depend}敌方拉近身前[{round(self.value1)}]'
        else:   # 未知效果
            result = '未知效果, 请至github反馈'
            self.error = f'ChangePos:detail1={self.detail1}'
        return result

    def Heal(self):
        result = '使'
        target, position, target_type, target_count, range_ = self.get_target()
        result += target
        result += 'HP回复'
        count = self.value2 + self.value3 * self.lvl + self.value4 * max(self.atk, self.mag_atk)
        count = round(count)
        result += f'[{count}]<{self.value2} + {self.value3} * 技能等级 + {self.value4} * 攻击力>'
        return result

    def Barrier(self):
        result = '对'
        target, position, target_type, target_count, range_ = self.get_target()
        if range_:
            result += range_
            result += '内'
        else:
            if position:
                result += position
        if target_type:
            result += target_type
        result += target_count
        result += target
        result += '展开'
        if self.detail1 == 1:   # 1: 物理无效护盾
            result += '无效物理伤害的护盾'
        elif self.detail1 == 2: # 2: 魔法无效护盾
            result += '无效魔法伤害的护盾'
        elif self.detail1 == 3: # 3: 物理吸收护盾
            result += '吸收物理伤害的护盾'
        elif self.detail1 == 4: # 4: 魔法吸收护盾
            result += '吸收魔法伤害的护盾'
        elif self.detail1 == 5: # 5: 物理和魔法无效护盾
            result += '无效物理和魔法伤害的护盾'
        elif self.detail1 == 6: # 6: 物理和魔法吸收护盾
            result += '吸收物理和魔法伤害的护盾'
        else:   # 7: 未知
            result = '未知护盾类型, 请至github反馈'
            self.error = f'Barrier:detail1={self.detail1}'
        count = self.value1 + self.value2 * self.lvl
        count = round(count)
        result += f'[{count}]<{self.value1} + {self.value2} * 技能等级>，持续[{self.value3}秒]'
        return result

    def ChooseEnemy(self):
        result = '锁定'
        target, position, target_type, target_count, range_ = self.get_target()
        if position:
            result += position
        result += target
        return result

    def Speed(self):
        if self.detail1 == 1:   # 1: 减速
            ailment = '减速'
        elif self.detail1 == 2: # 2: 加速
            ailment = '加速'
        elif self.detail1 == 3: # 3: 麻痹
            ailment = '麻痹'
        elif self.detail1 == 4: # 4: 冻结
            ailment = '冻结'
        elif self.detail1 == 5: # 5: 束缚
            ailment = '束缚'
        elif self.detail1 == 6: # 6: 睡眠
            ailment = '睡眠'
        elif self.detail1 == 7 or self.detail1 == 12 or self.detail1 == 14: # 7: 眩晕
            ailment = '眩晕'
        elif self.detail1 == 8: # 8: 石化
            ailment = '石化'
        elif self.detail1 == 9: # 9: 拘留
            ailment = '拘留'
        elif self.detail1 == 10: # 10: 昏迷
            ailment = '昏迷'
        elif self.detail1 == 11: # 11: 时间停止
            ailment = '时间停止'
        elif self.detail1 == 13: # 13: 结晶
            ailment = '结晶'
        else:   # 14: 未知
            ailment = '未知效果, 请至github反馈'
        target, position, target_type, target_count, range_ = self.get_target()
        result = f'{ailment}{target}，速度变更为初始值的[{self.value1}]倍，持续[{self.value3}]秒'
        return result

    def Dot(self):
        result = '使'
        target, position, target_type, target_count, range_ = self.get_target()
        if self.depend_id:
            result += f'受到动作({self.depend_id % 100})影响的'
        result += target
        result += '进入'
        if self.detail1 == 0:   # 0: 拘留(造成伤害)
            result += '拘留(造成伤害)'
        elif self.detail1 == 1 or self.detail1 == 7: # 1: 中毒
            result += '中毒'
        elif self.detail1 == 2: # 2: 烧伤
            result += '烧伤'
        elif self.detail1 == 3 or self.detail1 == 8: # 3: 诅咒
            result += '诅咒'
        elif self.detail1 == 4: # 4: 猛毒
            result += '猛毒'
        elif self.detail1 == 5: # 5: 咒术
            result += '咒术'
        else:   # 未知
            result += '未知效果, 请至github反馈'
            self.error = f'Dot:detail1={self.detail1}'
        count = self.value1 + self.value2 * self.lvl
        count = round(count)
        result += f'状态，每秒造成伤害[{count}]<{self.value1} + {self.value2} * 技能等级>，'
        if self.value5:
            result += f'每秒增加基础数值的[{self.value5}%]，'
        result += f'持续[{self.value3}]秒'

    def Effect(self):
        result = ''
        depend = ''
        if self.depend_id:
            depend = f'受到动作({self.depend_id % 100})影响'
        target, position, target_type, target_count, range_ = self.get_target()
        result += depend
        if range_:
            result += range_
            result += '内'
        else:
            if position:
                result += position
        if self.id == 100901202:
            target_type = target_type.replace('的', '的敌方')
        if target_type and result:
            result += target_type
            target_type = ''
        result += target
        result += target_count
        if target_type:
            result += target_type
        effect_type = self.detail1 // 10 % 100
        if effect_type == 1:   # 1: 物理攻击力
            result += '物理攻击力'
        elif effect_type == 2: # 2: 物理防御力
            result += '物理防御力'
        elif effect_type == 3: # 3: 魔法攻击力
            result += '魔法攻击力'
        elif effect_type == 4: # 4: 魔法防御力
            result += '魔法防御力'
        elif effect_type == 5: # 5: 回避率
            result += '回避率提升'
        elif effect_type == 6: # 6: 物理暴击率
            result += '物理暴击率'
        elif effect_type == 7: # 7: 魔法暴击率
            result += '魔法暴击率'
        elif effect_type == 8: # 8: TP上升
            result += 'TP上升'
        elif effect_type == 9: # 9: HP吸收
            result += 'HP吸收'
        elif effect_type == 10: # 10: 移动速度
            result += '移动速度'
        elif effect_type == 11: # 11: 物理暴击伤害
            result += '物理暴击伤害'
        elif effect_type == 12: # 12: 魔法暴击伤害
            result += '魔法暴击伤害'
        elif effect_type == 13: # 13: 命中率
            result += '命中率'
        elif effect_type == 14: # 14: 受到暴击
            result += '受到暴击'
        elif effect_type == 16: # 16: 承受的物理伤害
            result += '承受的物理伤害'
        elif effect_type == 17: # 17: 承受的魔法伤害
            result += '承受的魔法伤害'
        elif effect_type == 18: # 18: 造成的物理伤害
            result += '造成的物理伤害'
        elif effect_type == 19: # 19: 造成的魔法伤害
            result += '造成的魔法伤害'
        else:   # 未知
            result = '未知效果, 请至github反馈'
            self.error = f'Effect:detail1={self.detail1}'
        up_down_str = ''
        if '下' in self.level_up_disp or '降' in self.description or self.detail1 % 10 == 1:
            up_down_str = '下降'
        elif '升' in self.level_up_disp or self.detail1 % 10 == 0:    
            up_down_str = '提升'
        else:
            up_down_str = f'未知操作，请至github反馈。action_id: {self.id}'
        result += up_down_str
        if self.value1 == 1:
            count = self.value2 + self.value3 * self.lvl
            count = round(count)
            result += f'[{count}]<{self.value2} + {self.value3} * 技能等级>'
        elif self.value1 == 2:
            result += f'[{self.value2}%]'
        else:
            result = '未知数值, 请至github反馈'
            self.error = f'Effect:value1={self.value1}'
        time = self.value4
        if time:
            result += f'，持续[{time}]秒'
        return result

    def IfSp(self):
        result = '条件：'
        if self.detail2 != 0 or self.detail3 == 0:
            if self.detail1 > 0 and self.detail1 < 100:
                result += f'以[{int(self.detail1)}%]的概率使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 599:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}身上有持续伤害时，使用动作({int(self.detail2 % 100)})'
            elif (self.detail1 >= 600 and self.detail1 < 700) or (self.detail1 >= 6000 and self.detail1 < 7000):
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}的标记层数 ≥ [{max(1, int(self.value3))}] 时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 700:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}仅剩一名时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 > 700 and self.detail1 < 710:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'隐身状态的单位除外，{target}的数量是 [{int(self.detail1 - 700)}] 时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 720:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{range_}中存在单位时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 >= 901 and self.detail1 < 1000:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}的HP在 [{int(self.detail1 - 900)}%] 以下时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 1000:
                result += f'上一个动作击杀了单位时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 1001:
                result += f'技能暴击时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 >= 1200 and self.detail1 < 1300:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}的技能计数 ≥ [{int(self.detail1 % 10)}] 时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 1300 or self.detail1 == 2000:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}是 [物理攻击] 对象时，使用动作({int(self.detail2 % 100)})'
            elif self.detail1 == 2001:
                target, position, target_type, target_count, range_ = self.get_target()
                result += f'{target}是 [魔法攻击] 对象时，使用动作({int(self.detail2 % 100)})'
            else:
                target, position, target_type, target_count, range_ = self.get_target()
                status = {
                    100: '无法行动',
                    101: '加速状态',
                    200: '失明',
                    300: '魅惑状态',
                    400: '挑衅状态',
                    500: '烧伤状态',
                    501: '诅咒状态',
                    502: '中毒状态',
                    503: '猛毒状态',
                    504: '咒术状态',
                    511: '诅咒或咒术状态',
                    512: '中毒或猛毒状态',
                    710: 'BREAK 状态',
                    1400: '变身状态',
                    1600: '恐慌状态',
                    1601: '隐匿状态',
                    1700: '物理防御减少状态',
                    1701: '魔法防御减少状态',
                    721: '龙之眼状态',
                    1800: '多目标状态',
                    1900: '护盾展开',
                    3137: '界雷',
                    3162: '妨魔塵',
                    6160: '黏着状态',
                }
                result += f'当{target}在[{status.get(self.detail1, "未知状态")}]时，使用动作({int(self.detail2 % 100)})'
        if self.detail3 != 0:
            if self.detail1 > 0 and self.detail1 < 100:
                result += f'；以[{100 - int(self.detail1)}%]的概率使用动作({int(self.detail3 % 100)})'
        return result

    def Seal(self):
        result = '对'
        target, position, target_type, target_count, range_ = self.get_target()
        if range_:
            result += range_
            result += '内'
        else:
            if position:
                result += position
        if target_type:
            result += target_type
        result += target_count
        result += target
        if self.value4 > 0:
            result += f'追加[{int(self.value4)}]层标记，持续[{self.value3}]秒；叠加上限[{int(self.value1)}]'
        else:
            result += f'减少[{abs(int(self.value4))}]层标记，持续[{self.value3}]秒'
        return result

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
        count = round(count)
        result += f'[{count}]<{self.value2} + {self.value3} * 技能等级>'
        return result

    def action_type(self, action_type):
        result = ''
        # 拾取ERROR
        try:
            if action_type in skill_switch:
                result = getattr(self, skill_switch[action_type])()
            else:
                return f'未知技能类型, 请至github反馈。action_type: {action_type}'
            if self.error:
                result += f'存在bug, 请至github反馈。ERROR: {self.error}'
        except Exception as e:
            result = f'存在未知问题，请至github反馈。ERROR: {e}'
        return result