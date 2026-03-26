#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fake_id_card_number import IdCardNumber
import random

# 测试用例
def test_id_card():
    print("测试身份证号码处理功能")
    print("=" * 50)
    
    # 测试1: 随机生成身份证号
    print("1. 测试随机生成身份证号:")
    for i in range(5):
        random_sex = random.randint(0, 1)
        fake_id = IdCardNumber.fake_id(random_sex)
        print(f"  生成的身份证号: {fake_id}, 性别: {'男' if random_sex else '女'}")
    print()
    
    # 测试2: 验证身份证号
    print("2. 测试验证身份证号:")
    # 生成有效的身份证号
    valid_ids = [IdCardNumber.fake_id() for _ in range(3)]
    # 无效的身份证号
    invalid_ids = [
        '11010119900101123',  # 长度不足
        '1101011990010112345',  # 长度过长
        valid_ids[0][:-1] + 'X'  # 校验码错误
    ]
    
    for id_num in valid_ids:
        result = IdCardNumber.verify_id(id_num)
        print(f"  身份证号 {id_num}: {'有效' if result else '无效'}")
    
    for id_num in invalid_ids:
        result = IdCardNumber.verify_id(id_num)
        print(f"  身份证号 {id_num}: {'有效' if result else '无效'}")
    print()
    
    # 测试3: 身份证号信息提取
    print("3. 测试身份证号信息提取:")
    test_id = '110101199001011234'
    id_card = IdCardNumber(test_id)
    print(f"  身份证号: {test_id}")
    print(f"  区域名称: {id_card.get_area_name()}")
    print(f"  出生日期: {id_card.get_birthday()}")
    print(f"  出生日期(8位): {id_card.get_birth()}")
    print(f"  年龄: {id_card.get_age()}")
    print(f"  性别: {'男' if id_card.get_sex() else '女'}")
    print(f"  校验码: {id_card.get_check_digit()}")
    print(f"  出生日期是否有效: {'是' if id_card.is_valid_birthdate() else '否'}")
    print()
    
    # 测试4: 身份证号格式转换
    print("4. 测试身份证号格式转换:")
    eighteen_id = '110101199001011234'
    fifteen_id = IdCardNumber(eighteen_id).eighteen_to_fifteen()
    print(f"  18位转15位: {eighteen_id} -> {fifteen_id}")
    
    converted_eighteen = IdCardNumber(fifteen_id).fifteen_to_eighteen()
    print(f"  15位转18位: {fifteen_id} -> {converted_eighteen}")
    print()
    
    # 测试5: 输入验证
    print("5. 测试输入验证:")
    test_cases = [
        (123456, TypeError),  # 非字符串
        ('123456', ValueError),  # 长度不足
        ('1234567890123456789', ValueError)  # 长度过长
    ]
    
    for input_val, expected_exception in test_cases:
        try:
            IdCardNumber(input_val)
            print(f"  输入 {input_val}: 未抛出预期异常")
        except expected_exception as e:
            print(f"  输入 {input_val}: 正确抛出异常: {e}")
    print()
    
    print("测试完成!")

if __name__ == '__main__':
    test_id_card()
