# import urllib
import logging
import socket
import select
import datetime
import struct
import sd_notify
import local_notifier
import collections
import configargparse
import json
import os
import sys
# import csv
import time
from itertools import zip_longest
from collections import defaultdict
from websocket import create_connection
# from pint import UnitRegistry
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "tempest.log"


udp_rapid_wind = ['dateTime',
                  'windAvgms',
                  'windDir',
                  ]

udp_obs_st = ['dateTime',
              'windLullms',
              'windAvgms',
              'windGustms',
              'windDir',
              'windSampInt',
              'StnPressure',
              'airTempC',
              'RelHumidity',
              'illumlux',
              'ultraviolet',
              'solarRad',
              'rainAccum',
              'precipType',
              'lightnDistkm',
              'lightnCount',
              'battVolt',
              'reportIntm',
              ]

ws_obs_st = ['dateTime',
             'windLullms',
             'windAvgms',
             'windGustms',
             'windDir',
             'windSampInt',
             'StnPressure',
             'airTempC',
             'RelHumidity',
             'illumlux',
             'ultraviolet',
             'solarRad',
             'rainAccum',
             'precipType',
             'lightnDistkm',
             'lightnCount',
             'battVolt',
             'reportIntm',
             'dailyRainAccum',
             'RainAccumChk',
             'LocalRainAccumChk',
             'PrecipType',
             ]

LastRainSend = 0
hhour = 0
hhour9 = 0
hourRain = 0
dayRain = 0
day9Rain = 0
hourRainlist = [0] * 60
dayRainList = [0] * 24
day9RainList = [0] * 24
# Constants
# Height above sea level m
hasl = 160
# Height above ground level m
hagl = 6
# gravity m/s
grav = 9.80665
# gasconst ait  J/(kg K)
gasconst = 287.053
# Temp lapse rate near sea level (<11000m) K/m
tLapse = -0.0065
# swap the sign for -
atLapse = 0.0065
# standard Sea Level Temp K
slTemp = 288.15
# standard Sea Level Pres mb
slPres = 1013.25
constsexp = grav / (gasconst * atLapse)
constsinv = (gasconst * atLapse) / grav

# ip/port to listen to
BROADCAST_IP = '239.255.255.250'
BROADCAST_PORT = 50222


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def get_logger_file(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


# create broadcast listener socket
def create_broadcast_listener_socket(broadcast_ip, broadcast_port):

    b_sock = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    b_sock.bind(('', broadcast_port))

    mreq = struct.pack("4sl", socket.inet_aton(
        broadcast_ip), socket.INADDR_ANY)
    b_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return b_sock


def write_data(filename, data):
    fields = []
    fields.append("%03d" % int(data['windDir']))
    fields.append("/%03d" % int(data['windSpeed']))
    fields.append("g%03d" % int(data['windGust']))
    fields.append("t%03d" % int(data['outTemp']))
    fields.append("r%03d" % int(data['hourRain'] * 100))
    fields.append("p%03d" % int(data['rain24'] * 100))
    fields.append("P%03d" % int(data['dayRain'] * 100))
    if data['outHumidity'] < 0 or 100 <= data['outHumidity']:
        data['outHumidity'] = 0
    fields.append("h%02d" % int(data['outHumidity']))
    fields.append("b%05d" % int(data['barometer'] * 10))
    luminosity = int(data['solarRad'])
    if luminosity < 1000:
        fields.append("L%03d" % luminosity)
    else:
        luminosity -= 1000
        fields.append("l%03d" % luminosity)

    with open(filename, 'w') as f:
        f.write(time.strftime("%b %d %Y %H:%M\n",
                              time.localtime(data['dateTime'])))
        f.write(''.join(fields))
        f.write("\n")


def convertJSONStringToSequence(source):
    j = json.JSONDecoder(
        object_pairs_hook=collections.OrderedDict).decode(source)
    return j


def connectudp():
    my_logger.debug('Opening UDP connection...')
    # create the listener socket
    sock_list = [create_broadcast_listener_socket(
        BROADCAST_IP, BROADCAST_PORT)]
    return sock_list


def readudp(socklist):
    # small sleep otherwise this will loop too fast between messages and eat a lot of CPU

    time.sleep(0.1)

    # wait until there is a message to read
    readable, writable, exceptional = select.select(socklist, [], socklist, 0)

    # for each socket with a message
    for s in readable:
        data, addr = s.recvfrom(4096)

        # convert data to json
        data_json = json.loads(data)
        my_logger.debug('data_json record {} '.format(data_json))

        if data_json['type'] == 'obs_st':
            # takes the map list and the list of observations and creates a dictionary with the first value in
            #  the map as the key and the first value in the list of observations as the value, second value
            #  to second value, etc
            obsdata = data_json['obs'][0]
            obsdict = dict(zip_longest(udp_obs_st, obsdata))

            print(f'{dict(obsdict)}\n')
            extractobs(obsdict)
            # extractobs(obsdata)
            return

        elif data_json['type'] == 'evt_precip':
            time.sleep(5)
            return

        elif data_json['type'] == 'evt_strike':
            time.sleep(5)
            return

        elif data_json['type'] == 'rapid_wind':
            time.sleep(5)
            return

        elif data_json['type'] == 'obs_air':
            time.sleep(5)
            return

        elif data_json['type'] == 'obs_sky':
            time.sleep(5)
            return
        elif data_json['type'] == 'device_status':
            time.sleep(5)
            return

        elif data_json['type'] == 'hub_status':
            time.sleep(5)
            return

        else:
            my_logger.debug(
                'unexpected type data_json record {} '.format(data_json))
            time.sleep(5)
            return


def connectws():

    my_logger.debug('Opening Websocket connection...')

    ws = create_connection(
        'wss://ws.weatherflow.com/swd/data?api_key=' + options.personal_token)
    result = ws.recv()
    # print("Received '%s'" % result)
    # print('')

    my_logger.debug('Listening... ')
    ws.send('{"type":"listen_start",' + ' "device_id":' +
            options.tempest_ID + ',' + ' "id":"Tempest"}')
    result = ws.recv()
    my_logger.debug('Received {} '.format(result))
    print('')
    return ws


def readws(ws):

    my_logger.debug('Receiving Tempest data...')
    result = ws.recv()
    weatherJSON = json.JSONDecoder().decode(result)
    my_logger.debug(weatherJSON)
    obstype = weatherJSON['type']
    obsdata = weatherJSON['obs'][0]
    my_logger.debug(f'{obstype} {obsdata}')
    if obstype == 'obs_st':
        obsdict = dict(zip_longest(ws_obs_st, obsdata))

        print(f'{dict(obsdict)}\n')
        extractobs(obsdict)
        # print(f'{wxdict['windSpeed']}')
    return obsdata


def extractobs(obsdata):
    global LastRainSend
    global hourRainlist
    global dayRainList
    global day9RainList
    global hhour
    global hhour9
    global hourRain
    global dayRain
    global day9Rain

    if len(obsdata) < 18:
        my_logger.debug('obsdata short list {} '.format(len(obsdata)))
        return

    wxdata = defaultdict(dict)
    wxdata['dateTime'] = obsdata['dateTime']
    wxdata['windSpeed'] = obsdata['windAvgms'] * 2.23694    # convertit
    wxdata['windGust'] = obsdata['windGustms'] * 2.23694  # convertit
    wxdata['windDir'] = obsdata['windDir']
    wxdata['outTemp'] = (obsdata['airTempC'] * 9 / 5) + 32
    wxdata['outHumidity'] = obsdata['RelHumidity']
    wxdata['solarRad'] = obsdata['solarRad']
    datestamp = datetime.datetime.fromtimestamp(obsdata['dateTime'])
    omin = int(datestamp.strftime('%M'))
    ohour = int(datestamp.strftime('%H'))
    if ohour != hhour:
        hhour9 = hhour - 9
        if hhour9 < 0:
            hhour9 += 24
        day9RainList[hhour9] = hourRain
        dayRainList[hhour] = hourRain
        dayRainList[ohour] = 0
        dayRain = sum(dayRainList)
        day9Rain = sum(day9RainList[: hhour9])
        hhour = ohour
    hourRainlist[omin] = obsdata['rainAccum']
    hourRain = sum(hourRainlist)

    wxdata['hourRain'] = 0.0393701 * hourRain
    wxdata['dayRain'] = 0.0393701 * (day9Rain + hourRain)
    wxdata['rain24'] = 0.0393701 * (dayRain + hourRain)

    # Actual atmospheric pressure in hPa
    aap = obsdata['StnPressure']
    # Actual temperature in Celsius
    atc = obsdata['airTempC']
    # Temp in Kelvin K
    atk = atc + 273.15
    # constants defined above , here for readability
    # hasl = 168 grav = 9.80665 gasconst = 287.053 tLapse = -0.0065
    # atLapse = 0.0065 constsexp = grav/(gasconst*tLapse)
    a2tsx = aap * \
        (1 + ((atLapse * (hasl+hagl)) / (atk + atLapse * (hasl+hagl))))**constsexp
    a2ts = 1.0 * (aap * ((1 + (((slPres / aap)**constsinv)
                               * ((atLapse * (hasl+hagl)) / slTemp)))**constsexp))
    wxdata['barometer'] = a2ts
    my_logger.debug('aap {} atk {:3.2f} a2ts {:4.1f} a2tsx {:4.1f} humidity {}'.format(
        aap, atk, a2ts, a2tsx, wxdata['outHumidity']))

# in standard places (hasl from 100-800 m, temperature from -10 to 35)
# is the coeficient something close to hasl/10, meaning simply
# a2ts is about  aap + hasl/10

    my_logger.info('data time {} aap {} atc {} a2ts {:4.1f} a2ts {:4.1f} humidity {}'.format(
        wxdata['dateTime'], aap, atc,  a2ts, a2tsx, wxdata['outHumidity']))
    my_logger.info(
        f'\n day9RainList {day9RainList}\n dayRainList {dayRainList}\n hourRainlist {hourRainlist}')
    my_logger.info('\ndata time {} omin {} ohour {} hhour {} hhour9 {}\
    rain {:4.4f} hourRain {:4.4f} dayRain {:4.4f} day9Rain {:4.4f}'.format(
        datestamp.strftime('%c'), omin, ohour, hhour, hhour9, hourRainlist[omin], hourRain, dayRain, day9Rain))

    if LastRainSend < (int(wxdata['dateTime']) - 5 * 60):
        my_logger.debug(' LastRainSend over 5 min ')
        LastRainSend = int(wxdata['dateTime'])
        # print(weatherJSON['summary']['feels_like'])
        write_data('/tmp/wxnow.txt', wxdata)

    time.sleep(15)
    return


if __name__ == '__main__':
    scriptname = os.path.basename(__file__)
    print('started')

    p = configargparse.ArgParser(
        default_config_files=['/etc/default/tempest.conf', '~/.my_tempest'])
    p.add('--tempest_ID', required=False,  help='tempest station ID')
    p.add('--personal_token', required=False, help='tempest API token')
    p.add('--notctl', dest='notctl', action='store_true',
          help='run on direct not systemctl')
    p.add('--udp', dest='udp', action='store_true',
          help='run on run as udp connection')
    p.add('-l', '--log_level', default='WARNING',
          choices=['DEBUG', 'INFO', 'WARNING',
                   'ERROR', 'CRITICAL'],
          help='Log level for script')

    options = p.parse_args()

    if options.notctl:
        my_logger = get_logger_file(__name__)
        notify = local_notifier.Notifier()
    else:
        my_logger = get_logger(__name__)
        notify = sd_notify.Notifier()
    # my_logger.debug("a debug message")
    my_logger.setLevel(logging.INFO)
    my_logger.info('Logging level set ')
    if not notify.enabled():
        # Then it's probably not running is systemd with watchdog enabled
        raise Exception("Watchdog not enabled")

    # Report a status message
    notify.status("Initialising my service...")
    # time.sleep(3)
    # print(options)
    # logging.basicConfig(level=options.log_level)
    my_logger.setLevel(options.log_level)

    my_logger.debug('Logging level seems to include')
    my_logger.info('Logging level seems to include')
    my_logger.warning('Logging level seems to include')

    options = p.parse_args()
    my_logger.setLevel(options.log_level)

    notify.ready()
    notify.status("startingloop for requesters...")
    time.sleep(3)
    now = datetime.datetime.now()
    hhour = int(now.strftime('%H')) - 1

    if options.udp:
        socklist = connectudp()
    else:
        ws = connectws()

    while True:
        try:
            if options.udp:
                readudp(socklist)
            else:
                readws(ws)
        except Exception:
            my_logger.error('An error occurred', exc_info=True)
            exit(1)
