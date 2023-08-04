# USB CO2 Sensor reader

This is for IO Data's UD-CO2S USB CO2 sensor which equips CO2 sensor, humidity sendor and temperature sensor.
(My experience says only trusable sensor value is CO2.)


# Requirements

```
pip install pyserial
```

# how-to-use

```
usage: co2-sensor.py [-h] [-p PORT] [-l LOG] [-t] [-s SAMPLEDURATION] [-f FORMAT]

USB CO2 Sensor reader

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Set USB Serial Port e.g. /dev/tty.usbmodem101 or com1:, etc.
  -l LOG, --log LOG     Set log file
  -t, --time            Set this if need time
  -s SAMPLEDURATION, --sampleDuration SAMPLEDURATION
                        Set sample duration, print/log out exceed this
  -f FORMAT, --format FORMAT
                        Set output format json or csv```

```
$ python3 co2-sensor.py -p /dev/tty.usbmodem101 -l ./log.txt -t -s 2
```

```log.txt
[
  {"co2": "837", "humidity": "42.4", "temperature": "29.4", "time": "2023-06-14 21:13:13"},
  {"co2": "837", "humidity": "42.4", "temperature": "29.4", "time": "2023-06-14 21:13:15"},
  {"co2": "837", "humidity": "42.4", "temperature": "29.4", "time": "2023-06-14 21:13:17"},
]
```