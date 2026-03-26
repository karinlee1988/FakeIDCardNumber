#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/25 20:18
# @Author : karinlee
# @FileName : fake_id_card_number.py
# @Software : PyCharm
# @Blog : https://blog.csdn.net/weixin_43972976
# @github : https://github.com/karinlee1988/
# @gitee : https://gitee.com/karinlee/
# @Personal website : https://karinlee.cn/

import random
import re
from datetime import datetime, timedelta
# 导入区域信息
import area


class IdCardNumber:
    """
    用于对身份证号码进行处理
    20210801 test OK
    """

    def __init__(self, id_card_number: str):
        if not isinstance(id_card_number, str):
            raise TypeError("身份证号码必须是字符串类型")
        if not (len(id_card_number) == 15 or len(id_card_number) == 18):
            raise ValueError("身份证号码长度必须是15位或18位")
        self.id = id_card_number
        self.area_id = int(self.id[0:6])
        if len(self.id) == 18:
            self.birth_year = int(self.id[6:10])
            self.birth_month = int(self.id[10:12])
            self.birth_day = int(self.id[12:14])
        else:  # 15位身份证
            self.birth_year = int('19' + self.id[6:8])
            self.birth_month = int(self.id[8:10])
            self.birth_day = int(self.id[10:12])

    def get_area_name(self) -> str:
        """
        根据区域编号取出区域名称
        :return: 区域名称
        :rtype: str
        """
        return area.AREA_INFO[self.area_id]

    def get_birthday(self) -> str:
        """
        通过身份证号获取出生日期(只支持18位身份证，返回YYYY-MM-DD格式的日期字符串)
        :return: 出生日期
        :rtype: str
        """
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_birth(self) -> str:
        """
        通过身份证号码获取出生日期(返回8位日期字符串，支持15或18位身份证）
        :return: 出生日期
        :rtype: str
        """
        number_length = len(self.id)
        if number_length == 18:
            birth = self.id[6:14]
            return birth
        elif number_length == 15:
            birth = '19' + self.id[6:12]  # 目前的15位身份证是19xx年出生
            return birth
        else:
            return "ERROR"

    def get_age(self) -> int:
        """
        通过身份证号获取年龄
        :return: 年龄
        :rtype: int
        """
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self) -> int:
        """
        通过身份证号获取性别， 女生：0，男生：1
        :return: 性别代码
        :rtype: int
        """
        return int(self.id[16:17]) % 2

    def is_valid_birthdate(self) -> bool:
        """
        验证出生日期是否有效
        :return: 是否有效
        """
        try:
            datetime(self.birth_year, self.birth_month, self.birth_day)
            return True
        except ValueError:
            return False

    @staticmethod
    def calculate_check_digit(digital_ontology_code: str) -> str:
        """
        计算身份证号码校验码
        :param digital_ontology_code: 17位数字本体码
        :return: 校验码
        """
        if len(digital_ontology_code) != 17:
            raise ValueError("数字本体码必须是17位")
        
        wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 加权因子
        vi = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]  # 校验码对应值
        
        check_sum = sum(int(digital_ontology_code[i]) * wi[i] for i in range(17))
        remainder = check_sum % 11
        return str(vi[remainder])

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        if len(self.id) != 18:
            raise ValueError("只有18位身份证才有校验码")
        return self.calculate_check_digit(self.id[:17])

    @staticmethod
    def get_checkcode(digital_ontology_code: str) -> str:
        """
        静态方法，从身份证号码前17位数字本体码计算第18位校验码
        :param digital_ontology_code:   17位数字本体码
        :type digital_ontology_code: str
        :return str(vi[remainder]): 18位身份证的最后1位校验码
        :rtype str(vi[remainder]): str
        """
        try:
            return IdCardNumber.calculate_check_digit(digital_ontology_code)
        except ValueError:
            return False

    def fifteen_to_eighteen(self) -> str:
        """
        15位身份证转18位身份证

        15变18，就是出生年份由2位变为4位，最后加了一位用于验证。验证位的规则如下：
        1、将前面的身份证号码17位数分别乘以不同的系数。从第一位到第十七位的系数分别为:7. 9 .10 .5. 8. 4. 2. 1. 6. 3. 7. 9. 10. 5. 8. 4. 2.
        2、将这17位数字分别和系数相乘的结果相加。
        3、用加出来和除以11，看余数是多少?
        4 、余数只可能有0 、1、 2、 3、 4、 5、 6、 7、 8、 9、 10这11个数字。其分别对应的最后一位身份证的号码为1 .0. X. 9. 8. 7. 6. 5. 4. 3. 2.。
        5、通过上面得知如果余数是2，就会在身份证的第18位数字上出现罗马数字的Ⅹ。如果余数是10，身份证的最后一位号码就是2。

        :return: 18位身份证号码
        :rtype: str
        """
        if len(self.id) == 15:
            digital_ontology_code = self.id[0:6] + '19' + self.id[6:15]
            return digital_ontology_code + self.calculate_check_digit(digital_ontology_code)
        else:
            return "ERROR"

    def eighteen_to_fifteen(self) -> str:
        """
        18位身份证转15位身份证
        :return: 15位身份证
        :rtype: str
        """
        if len(self.id) == 18:
            # 去掉第6，7位和第18位即可18位身份证转15位身份证
            return self.id[0:6] + self.id[8:17]
        else:
            return "ERROR"

    @classmethod
    def verify_id(cls, id_card_number: str) -> bool:
        """
        校验身份证是否正确
        :param id_card_number: 身份证号码
        :return: 是否有效
        """
        # 验证格式
        if not re.match(area.ID_NUMBER_18_REGEX, id_card_number) and not re.match(area.ID_NUMBER_15_REGEX, id_card_number):
            return False
        
        # 验证18位身份证的校验码
        if len(id_card_number) == 18:
            try:
                check_digit = cls.calculate_check_digit(id_card_number[:17])
                return check_digit == id_card_number[-1].upper()
            except (ValueError, IndexError):
                return False
        
        return True

    @classmethod
    def fake_id(cls, sex: int = 0, area_number: int = 0):
        """
        随机生成身份证号，sex = 0表示女性，sex = 1表示男性
        生日在1960-2010区间
        """
        # 缓存区域码列表
        if not hasattr(cls, '_area_codes'):
            cls._area_codes = list(area.AREA_INFO.keys())
        
        # 选择区域码
        if area_number and area_number in area.AREA_INFO:
            id_card_number = str(area_number)
        else:
            id_card_number = str(random.choice(cls._area_codes))
        
        # 生成出生日期
        start, end = datetime(1960, 1, 1), datetime(2010, 12, 31)
        days_between = (end - start).days
        random_days = random.randint(0, days_between)
        birth_date = start + timedelta(days=random_days)
        birth_days = birth_date.strftime("%Y%m%d")
        id_card_number += birth_days
        
        # 生成顺序码和性别码
        id_card_number += str(random.randint(10, 99))  # 顺序码
        id_card_number += str(random.randrange(sex, 10, step=2))  # 性别码
        
        # 计算校验码
        return id_card_number + cls.calculate_check_digit(id_card_number)


if __name__ == '__main__':
    random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    # print(IdCardNumber.fake_id(random_sex,))  # 随机生成身份证号
    # print(IdCardNumber('410326199507103197').area_id)  # 地址编码:
    # print(IdCardNumber('654121198905094979').get_area_name())  # 地址:
    # print(IdCardNumber('654121198905094979').get_birthday())  # 生日:
    # print(IdCardNumber('654121198905094979').get_birth()) # 生日:
    # print(IdCardNumber('654121198905094979').get_age())  # 年龄:(岁)
    # print(IdCardNumber('654121198905094979').get_sex())  # 性别:(男)
    # print(IdCardNumber('654121198905094979').get_check_digit())  # 校验码:
    # print(IdCardNumber.verify_id('440228194610263439'))  # 检验身份证是否正确:
    # print(IdCardNumber('410326199507103197').eighteen_to_fifteen()) # 转为15位身份证：
    print(IdCardNumber('441822710307022').fifteen_to_eighteen())  # 转为18位身份证：