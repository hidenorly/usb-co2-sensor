# USB CO2 Sensor reader

This is for IO Data's UD-CO2S USB CO2 sensor which equips CO2 sensor, humidity sendor and temperature sensor.
(My experience says only trusable sensor value is CO2.)


# Requirements

```
pip install pyserial
```

# how-to-use

```
usage: co2-sensor.py [-h] [-p PORT] [-l LOG] [-t] [-s SAMPLEDURATION]

USB CO2 Sensor reader

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Set USB Serial Port e.g. /dev/tty.usbmodem101 or com1:, etc.
  -l LOG, --log LOG     Set log file
  -t, --time            Set this if need time
  -s SAMPLEDURATION, --sampleDuration SAMPLEDURATION
                        Set sample duration, print/log out exceed this
```

```
$ python3 co2-sensor.py -p /dev/tty.usbmodem101 -l ./log.txt -t -s 60
```

```log.txt
{"co2": "1017", "humidity": "41.6", "temperature": "29.0", "time": "2023-06-04 11:45:19"}
{"co2": "1017", "humidity": "41.6", "temperature": "29.0", "time": "2023-06-04 11:45:25"}
{"co2": "1016", "humidity": "41.6", "temperature": "29.0", "time": "2023-06-04 11:45:31"}
{"co2": "1016", "humidity": "41.6", "temperature": "29.0", "time": "2023-06-04 11:45:37"}
```