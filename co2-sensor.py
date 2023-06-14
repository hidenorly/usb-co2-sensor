#!/usr/bin/env python3
# coding: utf-8

#   Copyright 2023 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import serial
import serial.serialutil
import json
from datetime import datetime
import time

class SerialPort:
    def __init__(self, port, baudrate, timeoutSec = None):
        self.port = port
        self.baudrate = baudrate
        self.timeoutSec = timeoutSec
        self.uart = None
        self.reopen()

    def reopen(self):
        if self.uart==None or not self.uart.isOpen():
            if self.timeoutSec:
                self.uart = serial.Serial(self.port, self.baudrate, timeout=self.timeoutSec)
            else:
                self.uart = serial.Serial(self.port, self.baudrate)

    def readLine(self):
        result = None
        if self.uart.isOpen():
            result = self.uart.readline()
        return result

    def readlineUtf8Trim(self):
        result = self.readLine()
        if result != None:
            result = result.decode('utf-8').strip()
        return result

    def write(self, data):
        if self.uart.isOpen():
            self.uart.write(data.encode('utf-8'))

    def writeLine(self, data):
        self.write(data+"\r\n")

    def close(self):
        if self.uart.isOpen():
            self.uart.close()


class UsbCo2Sensor:
    def __init__(self, port):
        self.uart = SerialPort(port, 115200, 5)
        self.uart.writeLine("STA")
        self.uart.readlineUtf8Trim()

    def getRawData(self):
        result = ""
        try:
            result = self.uart.readlineUtf8Trim()
        except serial.serialutil.SerialTimeoutException as e:
            print(f'error: {e}')

        except KeyboardInterrupt:
            self.close()

        return result

    def getVal(self, keyValue):
        _keyVal = keyValue.split("=")
        if len(_keyVal)==2:
            return _keyVal[1].strip()
        return keyValue

    def getParsedResult(self):
        result = None
        rawData = self.getRawData() #e.g. is "CO2=955,HUM=46.3,TMP=32.0"
        data = rawData.split(",")
        if len(data)==3:
            result = {
                "co2": self.getVal(data[0]),
                "humidity" : self.getVal(data[1]),
                "temperature" : self.getVal(data[2])
            }
        return result

    def close(self):
        self.uart.writeLine("STP")
        self.uart.close()


class Reporter:
    def __init__(self, stream = None):
        self.stream = stream

    def _print(self, data):
        if self.stream:
            self.stream.write( str(data) + "\n" )
        else:
            print( str(data) )

    def print(self, data):
        self._print(data)

    def close(self):
        if self.stream:
            self.stream.close()
        self.stream = None

    def __del__(self):
        if self.stream:
            self.close()


class JsonReporter(Reporter):
    def __init__(self, stream = None):
        super().__init__(stream)
        self._print("[")

    def print(self, data):
        self._print( "\t" + json.dumps(data) + "," )

    def close(self):
        self._print("]")
        super().close()


class CsvReporter(Reporter):
    def __init__(self, stream = None, enableColumnFirstLine = False):
        super().__init__(stream)
        self.alreadyColumnOutput = False

    def print(self, data):
        if not self.alreadyColumnOutput:
            self.alreadyColumnOutput = True
            columns = "#" + ",".join(data.keys())
            if columns!="#":
                self._print(columns)
        self._print( ",".join(data.values()) )


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='USB CO2 Sensor reader')
    parser.add_argument('-p', '--port', action='store', default="/dev/tty.usbmodem101", help='Set USB Serial Port e.g. /dev/tty.usbmodem101 or com1:, etc.')
    parser.add_argument('-l', '--log', action='store', default=None, help='Set log file')
    parser.add_argument('-t', '--time', action='store_true', default=False, help='Set this if need time')
    parser.add_argument('-s', '--sampleDuration', type=int, action='store', default=1, help='Set sample duration, print/log out exceed this')
    parser.add_argument('-f', '--format', action='store', default="json", help='Set output format json or csv')
    args = parser.parse_args()

    sensor = UsbCo2Sensor(args.port)
    logOut = None
    if args.log:
        logOut = open(args.log, "a", encoding="utf-8")
    reporter = Reporter
    if args.format == "json":
        reporter = JsonReporter
    elif args.format == "csv":
        reporter = CsvReporter
    reporter = reporter(logOut)

    result = True
    lastTime = time.time()
    while(result):
        result = sensor.getParsedResult()
        nowTime = time.time()
        if result:
            if args.time:
                result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if (nowTime - lastTime) >= args.sampleDuration:
                lastTime = nowTime
                reporter.print( result )

    reporter.close()
