#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import traceback
from app.dao.train_op import *
from app.config.errorcode import *
from app.utils.utils import *


class TrainService(object):

    def __init__(self):
        self.__train_op = TrainOperation()

    def query_train(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__train_op.query_train(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def query_train_source(self):
        try:
            ret_code, ret_data = self.__train_op.query_train_source()
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict

    def delete_train(self, body):
        try:
            form = json.loads(body)
            ret_code, ret_data = check_value(form)
            if OP_SUCCESS == ret_code:
                ret_code, ret_data = self.__train_op.delete_train(form)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception, ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
