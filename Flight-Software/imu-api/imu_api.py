#!/usr/bin/env python3

# Copyright 2018 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

"""
API for interacting with IMU.


"""

import binascii
import socket
import struct
import time
import i2c
import subprocess

#############
# Config Data
DELAY = 0.200 #Prob need to change it as well
HEADER_SIZE = 5 #Prob need to change it as well
UDP_IP = "127.0.0.1"
UDP_PORT = 5007

TELEMETRY = {
    "general_data": {
        "a_x":                  {"command": "DATA:TEL? 0,data", "length": 4, "parsing": "<f"},
        "a_y":                  {"command": "DATA:TEL? 1,data", "length": 4, "parsing": "<f"},
        "a_z":                  {"command": "DATA:TEL? 2,data", "length": 4, "parsing": "<f"},
        "r_x":                  {"command": "DATA:TEL? 3,data", "length": 4, "parsing": "<f"},
        "r_y":                  {"command": "DATA:TEL? 4,data", "length": 4, "parsing": "<f"},
        "r_z":                  {"command": "DATA:TEL? 5,data", "length": 4, "parsing": "<f"},
        "temp":                 {"command": "DATA:TEL? 6,data", "length": 4, "parsing": "<f"},
        # "time_h":               {"command": "DATA:TEL? 7,data", "length": 4, "parsing": "<H"},
        # "time_m":               {"command": "DATA:TEL? 8,data", "length": 4, "parsing": "<H"},
        # "time_s":               {"command": "DATA:TEL? 9,data", "length": 4, "parsing": "<H"},
        # "time_ns":              {"command": "DATA:TEL? 10,data", "length": 4, "parsing": "<i"},
    }
}
# End Config Data
#################


class IMU:

    def __init__(self, ip, port):
        """
        Sets the bus number and stores the address
        """
        # self.i2cfile = i2c.I2C(bus=I2C_BUS_NUM)
        # self.address = address
        self.udp_ip = ip
        self.udp_port = port


    def read(self):

        subprocess.call(["./imu","XsensIMU.cpp","XsensIMU.h","imutest.cpp","to","imu"])
        # might not actually be compiling but just calling ./imu
        # return self.i2cfile.read(device=self.address, count=count)


    def read_telemetry(self):
        """
        Creates the output_dict, reads the data, inputs it into parsing mehods,
        then inserts and formats it in the output_dict.
        """
        # Create empty dictionary
        # output_dict = {}
        # for telem_field in dict:

            # input_dict = dict[telem_field]
            # Write command for the imu to prepare the data
            # self.write(input_dict['command'])
            # Delay time specified in the config parameter
            # (specified in the Pumpkin Firmware Reference Manual)
            # time.sleep(DELAY)
            # Read the data
            # raw_read_data = self.read(count=input_dict['length']+HEADER_SIZE)
            # Check and parse the header into a formatted dict
            # read_data = self._header_parse(raw_read_data)
            # Parse the data

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.udp_port))

        output_dict = {}
        self.read()

        data, addr = sock.recvfrom(1024)
        # parsed_data = self._unpack(
        #     parsing=input_dict['parsing'],
        #     data=read_data['data'])
        ax = struct.unpack('f', data[0:4])
        ay = struct.unpack('f', data[4:8])
        az = struct.unpack('f', data[8:12])
        rx = struct.unpack('f', data[12:16])
        ry = struct.unpack('f', data[16:20])
        rz = struct.unpack('f', data[20:24])
        #temperature
        temp = struct.unpack('f', data[24:28])
        #Convert to short (2 bytes)
        # hr min sec
        time_h = struct.unpack('H', data[28:30])
        time_m = struct.unpack('H', data[30:32])
        time_s = struct.unpack('H', data[32:34])
        timestamp = time_h[0] + time_m[0]/60 + time_s[0]/3600

        data_array = [ax[0], ay[0], az[0], rx[0], ry[0], rz[0], temp[0]]
        data_strings  = ['a_x', 'a_y', 'a_z', 'r_x', 'r_y', 'r_z', 'temp']

        if len(data_array) > 1:

            for index in range(len(data_array)):
                output_dict.update(
                    {data_strings[index]: {
                    'timestamp': timestamp,
                    'data': data_array[index]}})


        else:

            raise KeyError(
                "Number of data names doesn't match total data: " +
                len(data_array))

        print(output_dict)
        return output_dict


    def _format_data(self, telem_field, input_dict, read_data, parsed_data):
        """
        Takes in the read data, parsed data, and the input dictionary and outputs
        a formatted dictionary in the form of:
        {
            'fieldname': {'timestamp': int,'data': parsed data},
            etc...
        }
        """
        output_dict = {}
        if "names" in input_dict:
            if len(parsed_data) == 1:
                raise KeyError(
                    "Only one item parsed but subfields are listed: " +
                    telem_field)
        if len(parsed_data) > 1:
            # Multiple items parsed
            if "names" not in input_dict:
                raise KeyError(
                    "Must be a names field when multiple items are parsed: " +
                    telem_field)
            if len(input_dict['names']) != len(parsed_data):
                raise KeyError(
                    "Number of field names doesn't match parsing strings: " +
                    telem_field)
            for ind, field in enumerate(input_dict['names']):
                output_dict.update(
                    {field: {
                        'timestamp': read_data['timestamp'],
                        'data': parsed_data[ind]}})

        else:
            # Single item parsed - pull in dict then update with parsed data.
            # Must be done in this order otherwise it generates a keyerror.
            output_dict[telem_field] = read_data
            output_dict[telem_field]['data'] = parsed_data[0]
        return output_dict
