__package__ = "pyevaljs3"

import os
import logging
from typing import List

from . import runtime
from . import exception
JSException = exception.JSException
_logger = logging.getLogger("JSEval")
__all__ = ['JSEval', 'Context']


class JSEval(runtime.AbstractRuntime):

    def __init__(self):
        self._source = ''

    def compile(self, source: str = None, suffix: str = None) -> "Context":
        """
        编译javascript源代码
        :param source: 源代码字符串或要读取的文件路径
        :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等
        :return: Context
        """
        if os.path.isfile(source):
           source = open(source, encoding="utf-8").read()

        if source is not None:
            self._source += source
        else:
            raise ValueError("js source code is empty")

        if not suffix:
            suffix = ".js"
        if not suffix.__contains__("."):
            suffix = "." + suffix

        return Context(self._source, suffix)

    def eval(self, code: str = None, ignore_output=False):
        """
        执行javascript代码, 返回其结果
        :param code:
        :param ignore_output:
        :return: Any
        """
        if code is None:
            return

        return self._eval(code, ignore_output)

    async def async_eval(self, code: str = None, ignore_output=False):
        """
        执行javascript代码, 返回其结果
        :param code:
        :param ignore_output:
        :return: Any
        """
        if code is None:
            return

        return await self._async_eval(code, ignore_output)


class Context(runtime.AbstractContext):

    def __init__(self, source: str = None, suffix: str = None):
        self._source = source
        self._suffix = suffix

    def call(self, func, *args, arg_list: List = None):
        """
        调用指定的函数, 返回其结果
        :param func: 函数名
        :param args: 函数的参数列表
        :param arg_list: 函数的参数列表
        :return:
        """
        if arg_list is not None:
            _args = arg_list
        else:
            _args = [arg for arg in args]

        return self._call(func, _args)

    async def async_call(self, func, *args, arg_list: List = None, async_js_func: bool = False):
        """
        调用指定的函数, 返回其结果
        :param func: 函数名
        :param args: 函数的参数列表
        :param arg_list: 函数的参数列表
        :param async_js_func: 调用的js函数是否是异步js函数
        :return:
        """
        if arg_list is not None:
            _args = arg_list
        else:
            _args = [arg for arg in args]

        return await self._async_call(func, _args, async_js_func)
