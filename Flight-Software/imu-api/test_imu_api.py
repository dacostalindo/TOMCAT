#!/usr/bin/env python3

# Copyright 2018 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

"""
API for interacting with IMU.

Unit test module for the IMU api
"""

import unittest
import imu_api
import mock

############################
# Testing configuration data

UDP_IP = "127.0.0.1"
UDP_PORT = 5007

imu_api.DELAY = 0
imu_api.HEADER_SIZE = 5
# imu_api.TELEMETRY = {
#     "supervisor": {},
#     "module_1": {
#         "field_1": {"command": "TESTCOMMAND", "length": 2, "parsing": "hex"},
#         "field_2": {"command": "TESTCOMMAND", "length": 2, "parsing": "str"},
#         "field_3": {"command": "TESTCOMMAND", "length": 2, "parsing": "<H"},
#         "field_4": {"command": "TESTCOMMAND", "length": 4, "parsing": "<HH",
#                     "names": ["subfield_1", "subfield_2"]}
#     }
# }
# print(imu_api.TELEMETRY)
class TestIMUAPI(unittest.TestCase):

    def setUp(self):
        self.imu = imu_api.IMU(ip=UDP_IP,port=UDP_PORT)

    # def test_command_type(self):
    #     with self.assertRaises(TypeError):
    #         bad_command = 23  # Not a string
    #         self.imu.write(command=bad_command)

    # def test_stopbyte_appending(self):
    #     fake_command = b'SUP:LED ON'
    #     with mock.patch('i2c.I2C.write') as mock_i2cwrite:
    #         self.imu.write(command=fake_command)
    #         mock_i2cwrite.assert_called_with(
    #             data=fake_command + b'\x0a',
    #             device=self.imu.address)
    #
    # def test_read(self):
    #     read_count = 20
    #     with mock.patch('i2c.I2C.read') as mock_i2cread:
    #         self.imu.read(count=read_count)
    #         mock_i2cread.assert_called_with(
    #             device=self.imu.address,
    #             count=read_count)

    # def test_build_telemetry_dict_modulechecking(self):
    #     bad_module = "notamodule"
    #     good_fields = ["field_1"]
    #     with self.assertRaises(KeyError):
    #         self.imu._build_telemetry_dict(
    #             module=bad_module,
    #             fields=good_fields)
    #
    # def test_build_telemetry_dict_fieldchecking(self):
    #     bad_fields = ["notafieldname"]
    #     with self.assertRaises(KeyError):
    #         self.imu._build_telemetry_dict(
    #             module="module_1",
    #             fields=bad_fields)
    #
    # def test_build_telemetry_dict_all(self):
    #     requests_assert = imu_api.TELEMETRY['data']
    #     self.assertEqual(self.imu._build_telemetry_dict(
    #         module="data"),
    #         requests_assert)

    # def test_build_telemetry_dict_field(self):
    #     requests_assert = {}
    #     requests_assert['acceleration'] = \
    #         imu_api.TELEMETRY['data']['acceleration']
    #     self.assertEqual(
    #         self.imu._build_telemetry_dict(
    #             module="data",
    #             fields=["acceleration"]),
    #         requests_assert)
    # #
    # def test_header_parse_datareadyflag(self):
    #     notready_data = '\x00\x00\x00\x00\x00\x00'
    #     self.assertEqual(
    #         self.imu._header_parse(
    #             data=notready_data)['timestamp'],
    # #         0)
    #
    # def test_header_parse(self):
    #     data_ready = b'\x01'
    #     timestamp = b'\x02\x03\x04\x05'
    #     data = b'\x06'
    #     inputdata = data_ready+timestamp+data
    #     output_assert = {
    #         'timestamp': 841489.94,
    #         'data': b'\x06'
    #     }
    #     self.assertEqual(
    #         self.imu._header_parse(
    #             data=inputdata),
    #         output_assert)
    #
    # def test_unpack_str(self):
    #     result_data = 'this should be included'
    #     input_data = result_data + '\0this part \0should be \0cut off'
    #     output_assert = (result_data,)
    #     self.assertEqual(
    #         self.imu._unpack(
    #             parsing='str',
    #             data=input_data),
    #         output_assert)
    #
    # def test_unpack_hex(self):
    #     result_data = '00010203040506'
    #     input_data = '\x00\x01\x02\x03\x04\x05\x06'
    #     output_assert = (result_data,)
    #     self.assertEqual(
    #         self.imu._unpack(
    #             parsing='hex',
    #             data=input_data),
    #         output_assert)

    # def test_format_data_oneitem(self):
    #     fake_telem_field = 'field_1'  # Single item
    #     fake_input_dict = imu_api.TELEMETRY['module_1'][fake_telem_field]
    #     fake_timestamp = 100.00
    #     fake_read_data = {'timestamp': fake_timestamp, 'data': None}
    #     fake_data = 200
    #     fake_parsed_data = (fake_data,)
    #     output_assert = {fake_telem_field: {
    #         'timestamp': fake_timestamp,
    #         'data': fake_data}
    #     }
    #     self.assertEqual(
    #         self.imu._format_data(
    #             telem_field=fake_telem_field,
    #             input_dict=fake_input_dict,
    #             read_data=fake_read_data,
    #             parsed_data=fake_parsed_data
    #         ),
    #         output_assert)
    #
    # def test_format_data_multiitem(self):
    #     fake_telem_field = 'field_4'  # Has subfields
    #     fake_input_dict = imu_api.TELEMETRY['module_1'][fake_telem_field]
    #     fake_timestamp = 100.00
    #     fake_read_data = {'timestamp': fake_timestamp, 'data': None}
    #     fake_data1 = 100
    #     fake_data2 = 200
    #     fake_parsed_data = (fake_data1, fake_data2)
    #     output_assert = {
    #         'subfield_1': {
    #             'timestamp': fake_timestamp,
    #             'data': fake_data1},
    #         'subfield_2': {
    #             'timestamp': fake_timestamp,
    #             'data': fake_data2}
    #     }
    #     self.assertEqual(
    #         self.imu._format_data(
    #             telem_field=fake_telem_field,
    #             input_dict=fake_input_dict,
    #             read_data=fake_read_data,
    #             parsed_data=fake_parsed_data
    #         ),
    #         output_assert)
    #
    # def test_format_data_parsingrejection(self):
    #     fake_telem_field = 'field_4'  # Has subfields
    #     fake_input_dict = imu_api.TELEMETRY['module_1'][fake_telem_field]
    #     fake_read_data = {'timestamp': 100.00, 'data': None}
    #     bad_parsed_data = ('whatever stuff',)
    #     with self.assertRaises(KeyError):
    #         self.imu._format_data(
    #             telem_field=fake_telem_field,
    #             input_dict=fake_input_dict,
    #             read_data=fake_read_data,
    #             parsed_data=bad_parsed_data)
    #
    # def test_format_data_namesrejection(self):
    #     bad_telem_field = 'field_1'  # Single item
    #     fake_input_dict = imu_api.TELEMETRY['module_1'][bad_telem_field]
    #     fake_read_data = {'timestamp': 100.00, 'data': None}
    #     fake_parsed_data = (  # Multiple items
    #         'whatever stuff',
    #         'whatever other stuff'
    #     )
    #     with self.assertRaises(KeyError):
    #         self.imu._format_data(
    #             telem_field=bad_telem_field,
    #             input_dict=fake_input_dict,
    #             read_data=fake_read_data,
    #             parsed_data=fake_parsed_data)
    #
    # def test_format_data_lengthrejection(self):
    #     fake_telem_field = 'field_4'  # Single item
    #     fake_input_dict = imu_api.TELEMETRY['module_1'][fake_telem_field]
    #     fake_read_data = {'timestamp': 100.00, 'data': None}
    #     bad_parsed_data = (  # More than number of subfields
    #         'whatever stuff',
    #         'whatever other stuff',
    #         'and things'
    #     )
    #     with self.assertRaises(KeyError):
    #         self.imu._format_data(
    #             telem_field=fake_telem_field,
    #             input_dict=fake_input_dict,
    #             read_data=fake_read_data,
    #             parsed_data=bad_parsed_data)
    #

    def test_read_telemetry(self):
        module = 'general_data'
        field = 'all'
        # print(self.imu.read_telemetry_items(module=module,fields=fields))
        self.imu.read_telemetry()


        # fields = [field]
        # input_assert = {}
        # input_assert[field] = imu_api.TELEMETRY[module][field]
        #
        # with mock.patch('imu_api.IMU._read_telemetry_items') as mock_read_telemetry_items:
        #     self.imu.read_telemetry(
        #         module=module,
        #         fields=fields)
        #     mock_read_telemetry_items.assert_called_with(
        #         dict=input_assert)
    #
    # def test_read_telemetry_items(self):
    #     module = 'module_1'
    #     field = 'field_2'
    #     fields = [field]
    #     input_dict = {}
    #     input_dict[field] = imu_api.TELEMETRY[module][field]
    #     output_data = b'this should be returned'
    #     fake_timestamp = 841489.94
    #     return_data = b'\x01\x02\x03\x04\x05' + output_data + \
    #         b'\0this \0should be \0cut off'
    #     output_assert = {field: {
    #         'timestamp': fake_timestamp,
    #         'data': output_data.decode()
    #     }}
    #     with mock.patch('imu_api.IMU.write') as mock_write, mock.patch('imu_api.IMU.read') as mock_read:
    #         mock_read.return_value = return_data
    #         self.assertEqual(
    #             self.imu._read_telemetry_items(dict=input_dict),
    #             output_assert)
    #

if __name__ == '__main__':
    unittest.main()
