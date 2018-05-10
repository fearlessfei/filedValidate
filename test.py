# *-* coding: utf-8 *-*

from base import (
    BaseField,
    BaseValidate,
)


class PhoneField(BaseField):

    _regular = '^1[3|4|5|7|8][0-9]\d{8}$'

    def __init__(self, name='', error_dict=None, required=True):
        error_msg_dict = {}
        if error_dict:
            error_msg_dict.update(error_dict)
        super(PhoneField, self).__init__(name=name, error_msg_dict=error_msg_dict, required=required)



class ListField(BaseField):

    _type = list

    def __init__(self, name='', error_dict=None, required=True):
        error_msg_dict = {}
        if error_dict:
            error_msg_dict.update(error_dict)

        super(ListField, self).__init__(name=name, error_msg_dict=error_msg_dict, required=required)


def test1(validate_data):
    class MyValidate(BaseValidate):
        phone = PhoneField()
        id_list = ListField()

    mv = MyValidate()
    return mv.check_valid(validate_data)


def test2(validate_data):
    class MyValidate(BaseValidate):
        phone = PhoneField(required=False)
        id_list = ListField()

    mv = MyValidate()
    return mv.check_valid(validate_data)


def test3(validate_data):
    class MyValidate(BaseValidate):
        phone = PhoneField(name="mobile_phone")
        id_list = ListField()

    mv = MyValidate()
    return mv.check_valid(validate_data)


def test4(validate_data):
    class MyValidate(BaseValidate):
        phone = PhoneField(error_dict={'required': '手机号不能为空！', 'valid': '手机号无效！'})
        id_list = ListField(error_dict={'required': 'id列表不能为空！', 'valid': 'id列表类型无效！'})

    mv = MyValidate()
    return mv.check_valid(validate_data)



if __name__ == '__main__':
    validate_data1 = dict(
        phone='',
        id_list=[1, 2, 3],
    )

    validate_data2 = dict(
        phone='13123456789',
        id_list=[1, 2, 3],
    )

    validate_data3 = dict(
        mobile_phone='13123456789',
        id_list=[1, 2, 3],
    )

    validate_data3 = dict(
        mobile_phone='',
        id_list=[1, 2, 3],
    )

    validate_data4 = dict(
        mobile_phone='',
        id_list={"a": 1},
    )

    validate_data5 = dict(
        mobile_phone='abc',
        id_list=[1, 2, 3],
    )

    print test1(validate_data1)
    # (False, {'id_list': [1, 2, 3]}, {'phone': 'phone is required'})
    print test2(validate_data1)
    # (True, {'phone': '', 'id_list': [1, 2, 3]}, {})
    print test3(validate_data2)
    # (False, {'id_list': [1, 2, 3]}, {'mobile_phone': 'mobile_phone is required'})
    print test4(validate_data4)
    # (False, {}, {'phone': '\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba\xef\xbc\x81', 'id_list': 'id\xe5\x88\x97\xe8\xa1\xa8\xe7\xb1\xbb\xe5\x9e\x8b\xe6\x97\xa0\xe6\x95\x88\xef\xbc\x81'})
    print test4(validate_data5)
    # (False, {'id_list': [1, 2, 3]}, {'phone': '\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba\xef\xbc\x81'})
