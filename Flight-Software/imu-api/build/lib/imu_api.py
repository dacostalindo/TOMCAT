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

#############
# Config Data
DELAY = 0.200 #Prob need to change it as well
HEADER_SIZE = 5 #Prob need to change it as well
UDP_IP = "127.0.0.1"
UDP_PORT = 5007

TELEMETRY = {
    # "supervisor": {
    #     "firmware_version": {"command": "SUP:TEL? 0,data",  "length": 48, "parsing": "str"},
    #     "commands_parsed":  {"command": "SUP:TEL? 1,data",  "length": 8, "parsing": "<Q"},
    #     "scpi_errors":      {"command": "SUP:TEL? 2,data",  "length": 8, "parsing": "<Q"},
    #     "cpu_selftests":    {"command": "SUP:TEL? 4,data",  "length": 22, "parsing": "<QQhhh",
    #                          "names": ["selftest0", "selftest1", "selftest2", "selftest3", "selftest4"]},
    #     "time":             {"command": "SUP:TEL? 5,data",  "length": 8, "parsing": "<Q"},
    #     "context_switches": {"command": "SUP:TEL? 6,data",  "length": 8, "parsing": "<Q"},
    #     "idling_hooks":     {"command": "SUP:TEL? 7,data",  "length": 8, "parsing": "<Q"},
    #     "mcu_load":         {"command": "SUP:TEL? 8,data",  "length": 4, "parsing": "<f"},
    #     "serial_num":       {"command": "SUP:TEL? 9,data",  "length": 2, "parsing": "<H"},
    #     "i2c_address":      {"command": "SUP:TEL? 10,data",  "length": 1, "parsing": "<B"},
    #     "tuning":           {"command": "SUP:TEL? 11,data",  "length": 1, "parsing": "<b"},
    #     "nvm_write_cycles": {"command": "SUP:TEL? 12,data",  "length": 2, "parsing": "<H"},
    #     "reset_cause":      {"command": "SUP:TEL? 13,data", "length": 2, "parsing": "<H"}
    # },
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

    # def write(self, command):
    #     """
    #     Write command used to append the proper stopbyte to all writes.
    #     """
    #     if type(command) is str:
    #         command = str.encode(command)
    #
    #     if type(command) is bytes:
    #         return self.i2cfile.write(
    #             device=self.address, data=command+b'\x0A')
    #     else:
    #         raise TypeError('Commands must be str or bytes.')

    # def read(self, count):
    #     return self.i2cfile.read(device=self.address, count=count)

    def read_telemetry(self, module, fields=["all"]):
        """
        Read and parse specific fields from the MCUs that are contained in the
        config file.

        Input:
        module = string module name. Must exactly match the module name in the
        config file and the I2C address must be valid and non-zero. If address
        is 0, it assumes the module is not present/not configured.
        fields = list of strings, strings must exactly match fields in
        the config file listed in the "telemetry" section under "supervisor" or
        the specific module name. If field is left blank it defaults to ["all"],
        which pulls all available telemetry for that module.

        Output: A dict with keys for all fields requested with "timestamp" and
        "data" keys for each field.
        """
        requests = self._build_telemetry_dict(module=module, fields=fields)
        output = self._read_telemetry_items(dict=requests)
        return output

    def _build_telemetry_dict(self, module, fields=["all"]):
        """
        This method builds the dictionary of requested data.
        """
        if module not in TELEMETRY:
            # Check that module is listed in config file
            raise KeyError(
                'Module name: '+str(module)+' not found in imu_config file.')
        if type(fields) != list:
            # Validate fields input type
            raise TypeError(
                'fields argument must be a list of fieldnames from ' +
                'the configuration data. Input: ' + str(fields))

        module_telem = TELEMETRY[module]
        # supervisor_telem = TELEMETRY['supervisor']
        if fields == ["all"]:
            # Pulling all info
            requests = module_telem
            # requests.update(supervisor_telem)
            return requests

        # Builds requested dict
        # Validates fields input values
        requests = {}
        for field in fields:
            if field in module_telem:
                requests[field] = module_telem[field]
            # elif field in supervisor_telem:
            #     requests[field] = supervisor_telem[field]
            else:
                raise KeyError('Invalid field: '+str(field))
        return requests

    def _read_telemetry_items(self, dict):
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

            while True:

                read_data, addr = sock.recvfrom(1024)

                # parsed_data = self._unpack(
                #     parsing=input_dict['parsing'],
                #     data=read_data['data'])

                ax = struct.unpack('f', data[0:4]))
                ay = struct.unpack('f', data[4:8]))
                az = struct.unpack('f', data[8:12]))
                rx = struct.unpack('f', data[12:16]))
                ry = struct.unpack('f', data[16:20]))
                rz = struct.unpack('f', data[20:24]))
                #temperature
                temp = struct.unpack('f', data[24:28]))
                #Convert to short (2 bytes)
                # hr min sec
                time_h = struct.unpack('H', data[28:30]))
                time_m = struct.unpack('H', data[30:32]))
                time_s = truct.unpack('H', data[32:34]))
                timestamp = time_h + time_m + time_s

                data_array = [ax[0], ay[0], az[0], rx[0], ry[0], rz[0], temp[0]]
                data_strings  = ["a_x", "a_y", "a_z", "r_x", "r_y", "r_z", "temp"]

                # if len(parsed_data) > 1:
                #
                #     for index in len(data_array):
                #           output_dict.update(
                #               {data_strings[index]: {
                #                   'timestamp': timestamp,
                #                   'data': data_array[index]}})

            # output_dict.update(
            #     self._format_data(
            #         telem_field=telem_field,
            #         input_dict=input_dict,
            #         read_data=read_data,
            #         parsed_data=parsed_data))

        return output_dict

    # def _header_parse(self, data):
    #     """
    #     Parses the header data. Format is:
    #     [data ready flag][timestamp][data]
    #     output format is:
    #     {'timestamp':timestamp,'data':data}
    #     If the data ready flag is not set, it sets the timestamp to 0
    #     """
    #     if data[0] != 1:
    #         # Returns 0 for timestamp if data was not ready, but still returns
    #         # the data for debugging purposes.
    #         # telemetry data}
    #         return {'timestamp': 0, 'data': data[HEADER_SIZE:]}
    #
    #     # Unpack timestamp in seconds.
    #     timestamp = struct.unpack('<i', data[1:HEADER_SIZE])[0]/100.0
    #     # Return the valid packet timestamp and data
    #     return {'timestamp': timestamp, 'data': data[HEADER_SIZE:]}

    # def _unpack(self, parsing, data):
    #     """
    #     Basically just an abstraction of struct.unpack() to allow for types that
    #     are not standard in the method.
    #
    #     Input data read over I2C from a Pumpkin module and parsing string that
    #     indicates a special parsing method or is a valid format string for the
    #     python struct.unpack() method.
    #
    #     Outputs a tuple where each field is an item parsed.
    #     """
    #     if type(parsing) not in [str, bytes]:
    #         # Check that parsing is a valid type
    #         raise TypeError(
    #             'Parsing field must be a valid struct parsing string. Input: '
    #             + str(type(parsing)))
    #
    #     if type(data) is str:
    #         data = data.encode()
    #
    #     if parsing == "str":
    #         # Search for the null terminator,
    #         # return the leading string in a tuple
    #         str_data = data.split(b'\0')[0]
    #         return (str_data.decode(),)
    #     elif parsing == "hex":
    #         # Store as a hex string. This is so we can return binary data.
    #         # Return as a single field in a tuple
    #         return (binascii.hexlify(data).decode(),)
    #
    #     # All others parse directly with the parsing string.
    #     return struct.unpack(parsing, data)

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
