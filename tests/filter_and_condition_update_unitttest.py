# -*- coding: utf8 -*-

import unittest
from lib.ots2_api_test_base import OTS2APITestBase
import lib.restriction as restriction
from ots2 import *
from ots2.error import *
import time
import logging

class FilterAndConditionUpdateTest(OTS2APITestBase):
    TABLE_NAME = "test_filter_and_condition_update"

    """ConditionUpdate"""

    def test_update_row(self):
        """调用UpdateRow API, 构造不同的Condition"""
        table_name = FilterAndConditionUpdateTest.TABLE_NAME
        table_meta = TableMeta(table_name, [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)

    
        # 注入一行 index = 0
        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0)]
        row = Row(primary_key, attribute_columns)
        self.client_test.put_row(table_name, row)

        attribute_columns = {
            'put': [('index' , 0)]
        }
        # 注入一行，条件是index = 1时，期望写入失败
        row.attribute_columns = attribute_columns
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.EQUAL))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index = 0时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.EQUAL))
        self.client_test.update_row(table_name, row, condition)

        # 注入一行，条件是addr = china时，因为该列不存在，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("addr", "china", ComparatorType.EQUAL, False))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 再次注入一行，条件是addr = china时，同时设置如果列不存在则不检查，期望写入失败
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("addr", "china", ComparatorType.EQUAL, True))
        self.client_test.update_row(table_name, row, condition)

        ## NOT_EQUAL

        # 注入一行，条件是index != 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index != 1时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.NOT_EQUAL))
        self.client_test.update_row(table_name, row, condition)

        ## GREATER_THAN

        # 注入一行，条件是index > 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.GREATER_THAN))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index > -1时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", -1, ComparatorType.GREATER_THAN))
        self.client_test.update_row(table_name, row, condition)

        ## GREATER_EQUAL

        # 注入一行，条件是index >= 1时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.GREATER_EQUAL))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index >= 0时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.GREATER_EQUAL))
        self.client_test.update_row(table_name, row, condition)

        ## LESS_THAN

        # 注入一行，条件是index < 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.LESS_THAN))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index < 1 时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.LESS_THAN))
        self.client_test.update_row(table_name, row, condition)

        ## LESS_EQUAL

        # 注入一行，条件是index <= -1时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", -1, ComparatorType.LESS_EQUAL))
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index <= 0 时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.LESS_EQUAL))
        self.client_test.update_row(table_name, row, condition)

        ## COMPOSITE_CONDITION
        row.attribute_columns = {
            'put': [('index',0), ('addr','china')]
        }
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.update_row(table_name, row, condition)

        ## AND

        # 注入一行，条件是index == 0 & addr != china期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.AND)
            cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
            cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index == 0 & addr == china 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.update_row(table_name, row, condition)

        ## NOT

        # 注入一行，条件是!(index == 0 & addr == china)期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.NOT)
            sub_cond = CompositeCondition(LogicalOperator.AND)
            sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
            sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
            cond.add_sub_condition(sub_cond)

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是!(index != 0 & addr == china) 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.NOT)
        
        sub_cond = CompositeCondition(LogicalOperator.AND)
        sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
        cond.add_sub_condition(sub_cond)

        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.update_row(table_name, row, condition)

        ## OR

        # 注入一行，条件是index != 0 or addr != china期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.OR)
            cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
            cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.update_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index == 0 or addr != china 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.OR)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))
        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.update_row(table_name, row, condition)

    def test_put_row(self):
        """调用PutRow API, 构造不同的Condition"""
        table_name = FilterAndConditionUpdateTest.TABLE_NAME
        table_meta = TableMeta(table_name, [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)
    
        ## RelationCondition
        ## EQUAL
         
        # 注入一行 index = 0
        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0)]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row(table_name, row, condition)

        # 注入一行，条件是index = 1时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.EQUAL))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index = 0时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.EQUAL))
        self.client_test.put_row(table_name, row, condition)

        # 注入一行，条件是addr = china时，因为该列不存在，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("addr", "china", ComparatorType.EQUAL, False))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 再次注入一行，条件是addr = china时，同时设置如果列不存在则不检查，期望写入失败
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("addr", "china", ComparatorType.EQUAL, True))
        self.client_test.put_row(table_name, row, condition)

        ## NOT_EQUAL

        # 注入一行，条件是index != 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index != 1时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.NOT_EQUAL))
        self.client_test.put_row(table_name, row, condition)

        ## GREATER_THAN

        # 注入一行，条件是index > 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.GREATER_THAN))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index > -1时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", -1, ComparatorType.GREATER_THAN))
        self.client_test.put_row(table_name, row, condition)

        ## GREATER_EQUAL

        # 注入一行，条件是index >= 1时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.GREATER_EQUAL))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index >= 0时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.GREATER_EQUAL))
        self.client_test.put_row(table_name, row, condition)

        ## LESS_THAN

        # 注入一行，条件是index < 0时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.LESS_THAN))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index < 1 时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.LESS_THAN))
        self.client_test.put_row(table_name, row, condition)

        ## LESS_EQUAL

        # 注入一行，条件是index <= -1时，期望写入失败
        try:
            condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", -1, ComparatorType.LESS_EQUAL))
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index <= 0 时，期望写入成功
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.LESS_EQUAL))
        self.client_test.put_row(table_name, row, condition)

        ## COMPOSITE_CONDITION
        row.attribute_columns = [('index',0), ('addr','china')]
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row(table_name, row, condition)

        ## AND

        # 注入一行，条件是index == 0 & addr != china期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.AND)
            cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
            cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index == 0 & addr == china 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.put_row(table_name, row, condition)

        ## NOT

        # 注入一行，条件是!(index == 0 & addr == china)期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.NOT)
            sub_cond = CompositeCondition(LogicalOperator.AND)
            sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
            sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
            cond.add_sub_condition(sub_cond)

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是!(index != 0 & addr == china) 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.NOT)
        
        sub_cond = CompositeCondition(LogicalOperator.AND)
        sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
        cond.add_sub_condition(sub_cond)

        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.put_row(table_name, row, condition)

        ## OR

        # 注入一行，条件是index != 0 or addr != china期望写入失败
        try:
            cond = CompositeCondition(LogicalOperator.OR)
            cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
            cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

            condition = Condition(RowExistenceExpectation.IGNORE, cond)
            self.client_test.put_row(table_name, row, condition)
            self.assertTrue(False)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        # 注入一行，条件是index == 0 or addr != china 时，期望写入成功
        cond = CompositeCondition(LogicalOperator.OR)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))
        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.put_row(table_name, row, condition)

    def test_get_row(self):
        """调用GetRow API, 构造不同的Condition"""
        table_name = FilterAndConditionUpdateTest.TABLE_NAME
        table_meta = TableMeta(table_name, [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)
 
        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row(table_name, row, condition)

        ## COMPOSITE_CONDITION
        ## AND

        # 读取一行数据，(index != 0 & addr == china), 期望读取失败
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))

        cu, return_row,token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

        # 读取一行数据，(index == 0 & addr == china), 期望读取成功
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))

        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        ## OR

        # 读取一行数据，(index != 0 or addr != china), 期望读取失败
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

        # 读取一行数据，(index != 0 or addr == china), 期望读取成功
        cond = CompositeCondition(LogicalOperator.OR)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))

        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        ## NOT

        # 读取一行数据，!(index == 0 or addr == china), 期望读取失败
        cond = CompositeCondition(LogicalOperator.NOT)
        sub_cond = CompositeCondition(LogicalOperator.AND)
        sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))
        cond.add_sub_condition(sub_cond)

        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

        # 读取一行数据，!(index != 0 & addr != china), 期望读取成功
        cond = CompositeCondition(LogicalOperator.NOT)
        sub_cond = CompositeCondition(LogicalOperator.AND)
        sub_cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.NOT_EQUAL))
        sub_cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))
        cond.add_sub_condition(sub_cond)

        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        ## RELATION_CONDITION

        # 读取一行数据，index != 0, 期望读取失败
        cond = RelationCondition("index", 0, ComparatorType.NOT_EQUAL)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

        # 读取一行数据, index == 0, 期望读取成功
        cond = RelationCondition("index", 0, ComparatorType.EQUAL)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        # 读取一行数据, index >= 0, 期望读取成功
        cond = RelationCondition("index", 0, ComparatorType.GREATER_EQUAL)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        # 读取一行数据, index <= 0, 期望读取成功
        cond = RelationCondition("index", 0, ComparatorType.LESS_EQUAL)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(primary_key, return_row.primary_key)

        # 读取一行数据，index > 0, 期望读取失败
        cond = RelationCondition("index", 0, ComparatorType.GREATER_THAN)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

        # 读取一行数据，index < 0, 期望读取失败
        cond = RelationCondition("index", 0, ComparatorType.LESS_THAN)
        cu, return_row, token = self.client_test.get_row(table_name, primary_key, column_filter=cond, max_version=1)
        self.assertEqual(None, return_row)

    def test_delete_row(self):
        """调用DeleteRow API, 构造不同的Condition"""
        table_name = FilterAndConditionUpdateTest.TABLE_NAME
        table_meta = TableMeta(table_name, [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)

        # 注入一行 index = 0
        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0)]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row(table_name, row, condition)

        ## RELACTION_CONDITION

        # 读取一行数据，index < 0, 期望读取失败
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.LESS_THAN))

        try:
            self.client_test.delete_row(table_name, row, condition)
        except OTSServiceError, e:
            self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")


        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        try:
             self.client_test.delete_row(table_name, row, condition)
        except OTSServiceError, e:
             self.assert_error(e, 403, "OTSConditionCheckFail", "Condition check failed.")

        cond = CompositeCondition(LogicalOperator.OR)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.NOT_EQUAL))

        condition = Condition(RowExistenceExpectation.IGNORE, cond)
        self.client_test.delete_row(table_name, row, condition)


    def test_batch_write_row(self): 
        """调用BatchWriteRow API, 构造不同的Condition"""
        table_meta = TableMeta('myTable0', [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        table_meta = TableMeta('myTable1', [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)

        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',1)]
        attribute_columns = [('index',1), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',2)]
        attribute_columns = [('index',2), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',3)]
        attribute_columns = [('index',3), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)

        primary_key = [('gid',0), ('uid',4)]
        attribute_columns = [('index',4), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)

        primary_key = [('gid',0), ('uid',5)]
        attribute_columns = [('index',5), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)


        # put
        put_row_items = []
        put_row_items.append(PutRowItem(                
                Row([('gid',0), ('uid',0)], 
                    [('index',6), ('addr','china')]),
                Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.EQUAL))))

        put_row_items.append(PutRowItem(
            Row([('gid',0), ('uid',1)], 
                [('index',7), ('addr','china')]),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.EQUAL))))

        put_row_items.append(PutRowItem(                
            Row([('gid',0), ('uid',2)], 
                [('index',8), ('addr','china')]),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 2, ComparatorType.EQUAL))))

        batch_list = BatchWriteRowRequest()
        batch_list.add(TableInBatchWriteRowItem('myTable0', put_row_items))
        batch_list.add(TableInBatchWriteRowItem('myTable1', put_row_items))

        result = self.client_test.batch_write_row(batch_list)

        self.assertEqual(True, result.is_all_succeed())

        r0 = result.get_put_by_table('myTable0')
        r1 = result.get_put_by_table('myTable1')


        self.assertEqual(3, len(r0))
        self.assertEqual(3, len(r1))

        for i in r0:
            self.assertTrue(i.is_ok)
            self.assertEqual(1, i.consumed.write)
            self.assertEqual(1, i.consumed.read)

        for i in r1:
            self.assertTrue(i.is_ok)
            self.assertEqual(1, i.consumed.write)
            self.assertEqual(1, i.consumed.read)

        self.assertEqual(6, len(result.get_succeed_of_put()))
        self.assertEqual(0, len(result.get_failed_of_put()))

        # update
        update_row_items = []
        update_row_items.append(UpdateRowItem(                
            Row([('gid',0), ('uid',0)], 
                {
                        'put': [('index',9), ('addr','china')]
                }),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 0, ComparatorType.EQUAL))))

        update_row_items.append(UpdateRowItem(                
            Row([('gid',0), ('uid',1)], 
                {
                        'put': [('index',10), ('addr','china')]
                        }),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 1, ComparatorType.EQUAL))))


        update_row_items.append(UpdateRowItem(
            Row([('gid',0), ('uid',2)], 
            {
                'put': [('index',11), ('addr','china')]
            }),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 2, ComparatorType.EQUAL))))


        batch_list = BatchWriteRowRequest()
        batch_list.add(TableInBatchWriteRowItem('myTable0', update_row_items))
        batch_list.add(TableInBatchWriteRowItem('myTable1', update_row_items))

        result = self.client_test.batch_write_row(batch_list)

        self.assertEqual(False, result.is_all_succeed())

        r0 = result.get_update_by_table('myTable0')
        r1 = result.get_update_by_table('myTable1')

        self.assertEqual(3, len(r0))
        self.assertEqual(3, len(r1))

        for i in r0:
            self.assertFalse(i.is_ok)
            self.assertEqual("OTSConditionCheckFail", i.error_code)
            self.assertEqual("Condition check failed.", i.error_message)

        for i in r1:
            self.assertFalse(i.is_ok)
            self.assertEqual("OTSConditionCheckFail", i.error_code)
            self.assertEqual("Condition check failed.", i.error_message)


        self.assertEqual(0, len(result.get_succeed_of_update()))
        self.assertEqual(6, len(result.get_failed_of_update()))

        # delete
        delete_row_items = []
        delete_row_items.append(DeleteRowItem(               
            Row([('gid',0), ('uid',0)]),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 3, ComparatorType.EQUAL, False))))

        delete_row_items.append(DeleteRowItem(                
            Row([('gid',0), ('uid',1)]),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 4, ComparatorType.EQUAL, False))))

        delete_row_items.append(DeleteRowItem(                
            Row([('gid',0), ('uid',2)]),
            Condition(RowExistenceExpectation.IGNORE, RelationCondition("index", 5, ComparatorType.EQUAL, False))))

        batch_list = BatchWriteRowRequest()
        batch_list.add(TableInBatchWriteRowItem('myTable0', delete_row_items))
        batch_list.add(TableInBatchWriteRowItem('myTable1', delete_row_items))

        result = self.client_test.batch_write_row(batch_list)

        self.assertEqual(False, result.is_all_succeed())

        r0 = result.get_delete_by_table('myTable0')
        r1 = result.get_delete_by_table('myTable1')

        self.assertEqual(3, len(r0))
        self.assertEqual(3, len(r1))

        for i in r0:
            self.assertFalse(i.is_ok)
            self.assertEqual("OTSConditionCheckFail", i.error_code)
            self.assertEqual("Condition check failed.", i.error_message)

        for i in r1:
            self.assertFalse(i.is_ok)
            self.assertEqual("OTSConditionCheckFail", i.error_code)
            self.assertEqual("Condition check failed.", i.error_message)

        self.assertEqual(0, len(result.get_succeed_of_delete()))
        self.assertEqual(6, len(result.get_failed_of_delete()))
       
    def test_batch_get_row(self):
        """调用BatchGetRow API, 构造不同的Condition"""
        table_meta = TableMeta('myTable0', [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        table_meta = TableMeta('myTable1', [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)
 
        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',1)]
        attribute_columns = [('index',1), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',2)]
        attribute_columns = [('index',2), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable0', row, condition)

        primary_key = [('gid',0), ('uid',0)]
        attribute_columns = [('index',0), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)

        primary_key = [('gid',1), ('uid',0)]
        attribute_columns = [('index',1), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)

        primary_key = [('gid',2), ('uid',0)]
        attribute_columns = [('index',2), ('addr','china')]
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        self.client_test.put_row('myTable1', row, condition)


        ## COMPOSITE_CONDITION

        # 读取一行数据，(index != 0 & addr == china), 期望读取失败
        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 0, ComparatorType.EQUAL))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))

        column_to_get = ['index']
        
        batch_list = BatchGetRowRequest()

        primary_keys = []
        primary_keys.append([('gid',0), ('uid',0)])
        primary_keys.append([('gid',0), ('uid',1)])
        primary_keys.append([('gid',0), ('uid',2)])
        batch_list.add(TableInBatchGetRowItem('myTable0', primary_keys, column_to_get, cond, 1))

        primary_keys = []
        primary_keys.append([('gid',0), ('uid',0)])
        primary_keys.append([('gid',1), ('uid',0)])
        primary_keys.append([('gid',2), ('uid',0)])
        batch_list.add(TableInBatchGetRowItem('myTable1', primary_keys, column_to_get, cond, 1))

        result = self.client_test.batch_get_row(batch_list)
        table0 = result.get_result_by_table('myTable0')
        table1 = result.get_result_by_table('myTable1')

        self.assertEqual(6, len(result.get_succeed_rows()))
        self.assertEqual(0, len(result.get_failed_rows()))
        self.assertEqual(True, result.is_all_succeed())

        self.assertEqual(3, len(table0))
        self.assertEqual(3, len(table1))

        # myTable0
        # row 0
        self.assertEqual([('gid',0), ('uid',0)], table0[0].row.primary_key)
        self.assert_columns([('index',0)], table0[0].row.attribute_columns)

        # row 1
        self.assertEqual(None, table0[1].row.primary_key)
        self.assert_columns([], table0[1].row.attribute_columns)

        # row 2
        self.assertEqual(None, table0[2].row.primary_key)
        self.assert_columns([], table0[2].row.attribute_columns)

        # myTable1
        # row 0
        self.assertEqual([('gid',0), ('uid',0)], table1[0].row.primary_key)
        self.assert_columns([('index',0)], table0[0].row.attribute_columns)

        # row 1
        self.assertEqual(None, table1[1].row.primary_key)
        self.assert_columns([], table1[1].row.attribute_columns)

        # row 2
        self.assertEqual(None, table1[2].row.primary_key)
        self.assert_columns([], table1[2].row.attribute_columns)

        ## RELATION_CONDITION
        cond = RelationCondition('index', 0, ComparatorType.GREATER_THAN)
        column_to_get = ['index']
        
        batch_list = BatchGetRowRequest()

        primary_keys = []
        primary_keys.append([('gid',0), ('uid',0)])
        primary_keys.append([('gid',0), ('uid',1)])
        primary_keys.append([('gid',0), ('uid',2)])
        batch_list.add(TableInBatchGetRowItem('myTable0', primary_keys, column_to_get, cond, 1))

        primary_keys = []
        primary_keys.append([('gid',0), ('uid',0)])
        primary_keys.append([('gid',1), ('uid',0)])
        primary_keys.append([('gid',2), ('uid',0)])
        batch_list.add(TableInBatchGetRowItem('myTable1', primary_keys, column_to_get, cond, 1))

        result = self.client_test.batch_get_row(batch_list)

        self.assertEqual(6, len(result.get_succeed_rows()))
        self.assertEqual(0, len(result.get_failed_rows()))

        self.assertEqual(True, result.is_all_succeed())

        table0 = result.get_result_by_table('myTable0')
        table1 = result.get_result_by_table('myTable1')

        self.assertEqual(3, len(table0))
        self.assertEqual(3, len(table1))

        # myTable0
        # row 
        self.assertEqual(None, table0[0].row.primary_key)
        self.assert_columns([], table0[0].row.attribute_columns)

        # row 1
        self.assertEqual([('gid',0), ('uid',1)], table0[1].row.primary_key)
        self.assert_columns([('index', 1)], table0[1].row.attribute_columns)

        # row 2
        self.assertEqual([('gid',0), ('uid',2)], table0[2].row.primary_key)
        self.assert_columns([('index', 2)], table0[2].row.attribute_columns)

        # myTable1
        # row 0
        self.assertEqual(None, table1[0].row.primary_key)
        self.assert_columns([], table0[0].row.attribute_columns)

        # row 1
        self.assertEqual([('gid',1), ('uid',0)], table1[1].row.primary_key)
        self.assert_columns([('index', 1)], table1[1].row.attribute_columns)

        # row 2
        self.assertEqual([('gid',2), ('uid',0)], table1[2].row.primary_key)
        self.assert_columns([('index', 2)], table1[2].row.attribute_columns)


    def test_get_range(self):
        """调用GetRange API, 构造不同的Condition"""
        table_name = FilterAndConditionUpdateTest.TABLE_NAME
        table_meta = TableMeta(table_name, [('gid', ColumnType.INTEGER), ('uid', ColumnType.INTEGER)])
        table_options = TableOptions()
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        self.client_test.create_table(table_meta, table_options, reserved_throughput)

        time.sleep(5)
 
        for i in range(0, 100):
            primary_key = [('gid',0), ('uid',i)]
            attribute_columns = [('index',i), ('addr','china')]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            self.client_test.put_row(table_name, row, condition)

        ## COMPOSITE_CONDITION

        cond = CompositeCondition(LogicalOperator.AND)
        cond.add_sub_condition(RelationCondition("index", 50, ComparatorType.LESS_THAN))
        cond.add_sub_condition(RelationCondition("addr", 'china', ComparatorType.EQUAL))

        inclusive_start_primary_key = [('gid',INF_MIN), ('uid',INF_MIN)]
        exclusive_end_primary_key = [('gid',INF_MAX), ('uid',INF_MAX)]

        rows = []

        next_pk = inclusive_start_primary_key
        while next_pk != None:
            cu, next, row_list, token = self.client_test.get_range(
                table_name, 
                Direction.FORWARD, 
                next_pk, 
                exclusive_end_primary_key, 
                column_filter=cond,
                max_version=1)

            next_pk = next
            rows.extend(row_list)

        self.assertEqual(50, len(rows))
        for i in range(0, 50):
            r  = rows[i]

            self.assertEqual([('gid',0), ('uid',i)], r.primary_key)
            self.assert_columns([('addr','china'),('index',i)], r.attribute_columns)

        ## RELATION_CONDITION

        cond = RelationCondition("index", 50, ComparatorType.GREATER_EQUAL)

        inclusive_start_primary_key = [('gid',INF_MIN), ('uid',INF_MIN)]
        exclusive_end_primary_key = [('gid',INF_MAX), ('uid',INF_MAX)]
        consumed_counter = CapacityUnit()
        rows = []

        range_iterator = self.client_test.xget_range(
                table_name,
                Direction.FORWARD,
                inclusive_start_primary_key,
                exclusive_end_primary_key,
                consumed_counter,
                column_filter=cond,
                max_version=1) 

        for r in range_iterator:
            rows.append(r)

        self.assertEqual(50, len(rows))

        for i in range(50, 100):
            r  = rows[i -  50]

            self.assertEqual([('gid',0), ('uid',i)], r.primary_key)
            self.assert_columns([('addr','china'),('index',i)], r.attribute_columns)

if __name__ == '__main__':
    unittest.main()
