# *-* coding: utf-8 *-*

import re


class BaseField(object):

    _regular = None
    _type = None

    def __init__(self, error_msg_dict, required=False, name=''):
        self.is_valid = False
        self.value = None
        self.error = None
        self.name = name
        self.error_msg_dict = error_msg_dict
        self.required = required

    def validate(self, name, input_value):
        # 如果没有指定字段名字，字段名字默认是类属性的名字
        if not self.name:
            self.name = name
        if not self.required:
            # 允许输入内容为空
            self.is_valid = True
            # 输入的内容
            self.value = input_value
        else:
            # 输入的内容为空的情况
            if not input_value:
                # 默认如果有添错误信息
                if self.error_msg_dict.get('required', None):
                    self.error = self.error_msg_dict['required']
                else:
                    # 如果没有错误信息，就生成提示信息
                    self.error = "%s is required" % self.name
            else:
                # 根据正则表达式匹配
                if self._regular:
                    ret = re.match(self._regular, input_value)
                # 根据数据类型匹配
                elif self._type:
                    ret = isinstance(input_value, self._type)
                else:
                    raise NotImplementedError("Unkown check type")

                if ret:
                    # 匹配成功则返回True
                    self.is_valid = True
                    # 用户输入的内容
                    self.value = input_value
                else:
                    # 如果有自定义的错误信息，就提示错误信息
                    if self.error_msg_dict.get('valid', None):
                        self.error = self.error_msg_dict['valid']
                    else:
                        # 自动生成提示错误信息
                        self.error = "%s is invalid" % self.name


class BaseValidate:
    def check_valid(self, dict_data):
        flag = True
        error_msg_dict = {}
        success_value_dict = {}
        class_attrs = self.__class__.__dict__
        dict_attrs =  {k: class_attrs[k] for k in class_attrs
                        if not k.startswith('__')}

        for key, check in dict_attrs.items():
            # 待验证的数据可能不是字典，可能是一个obj
            # 根据待验证数据类型的不同可以通过子类继承重写check_valid方法或者
            # 添加基类构造方法通过传参的方式来判断待验证数据的类型来做对应的处理
            if check.name:
                key = check.name
            input_value = dict_data.get(key)

            check.validate(key, input_value)
            # 验证成功
            if check.is_valid:
                success_value_dict[key] = check.value
            else:
                error_msg_dict[key] = check.error
                # 表示验证不成功
                flag = False

        return flag, success_value_dict, error_msg_dict