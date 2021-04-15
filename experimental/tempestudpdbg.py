# import urllib
import logging
import socket
import select
import struct
import local_notifier
import collections
import configargparse
import json
import os
# mport csv
import time
import sys
from collections import defaultdict
# from websocket import create_connection
# from pint import UnitRegistry
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "tempestudpdbg.log"

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
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger
# notify = sd_notify.Notifier()
notify = local_notifier.Notifier()

# Constants
# Height above sea level m
hasl = 168
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


def extractobs(obsdata):
    if len(obsdata) < 22:
        my_logger.debug('obsdata short list {} '.format(len(obsdata)))
        return

    wxdata = defaultdict(dict)
    my_logger.debug('obsdata record {} '.format(obsdata))
    wxdata['dateTime'] = obsdata[0]
    windLullms = obsdata[1]
    windAvgms = obsdata[2]
    wxdata['windSpeed'] = windAvgms * 2.23694    # convertit
    windGustms = obsdata[3]
    wxdata['windGust'] = windGustms * 2.23694  # convertit
    wxdata['windDir'] = obsdata[4]
    windSampInt = obsdata[5]
    AirPressure = obsdata[6]
    airTempC = obsdata[7]
    wxdata['outTemp'] = (airTempC * 9 / 5) + 32
    wxdata['outHumidity'] = obsdata[8]
    illumlux = obsdata[9]
    ultravil = obsdata[10]
    solarRad = obsdata[11]
    rainAccum = obsdata[12]
    wxdata['hourRain'] = 0.0393701 * rainAccum
    precipType = obsdata[13]
    # 0=none, 1=rain, 2=hail
    lightnDistkm = obsdata[14]
    lightnCount = obsdata[15]
    battVolt = obsdata[16]
    reportIntm = obsdata[17]
    dailyRainAccum = obsdata[18]
    wxdata['dayRain'] = 0.0393701 * dailyRainAccum
    rainAccumFinal = obsdata[19]
    rainDailyAccumFinal = obsdata[20]
    wxdata['rain24'] = 0.0393701 * dailyRainAccum
    precipAnalType = obsdata[21]

    # Actual atmospheric pressure in hPa
    aap = AirPressure
    # Actual temperature in Celsius
    atc = airTempC
    # Temp in Kelvin K
    atk = atc + 273.15
    # constants defined above , here for readability
    # hasl = 168 grav = 9.80665 gasconst = 287.053 tLapse = -0.0065
    # atLapse = 0.0065 constsexp = grav/(gasconst*tLapse)
    a2tsx = aap * \
        (1 + ((atLapse * hasl) / (atk + atLapse * hasl)))**constsexp
    a2ts = 1.0 * (aap * ((1 + (((slPres / aap)**constsinv)
                               * ((atLapse * hasl) / slTemp)))**constsexp))
    my_logger.debug('aap {} atk {:3.2f} a2ts {:4.1f} a2tsx {:4.1f} humidity {}'.format(
        aap, atk, a2ts, a2tsx, wxdata['outHumidity']))
    wxdata['barometer'] = a2ts

# in standard places (hasl from 100-800 m, temperature from -10 to 35)
# is the coeficient something close to hasl/10, meaning simply
# a2ts is about  aap + hasl/10

    my_logger.info('data time {} aap {} atc {} a2ts {:4.1f} a2ts {:4.1f} humidity {}'.format(
        wxdata['dateTime'], aap, atc,  a2ts, a2tsx, wxdata['outHumidity']))

    # print(weatherJSON['summary']['feels_like'])
    write_data('/tmp/wxnow.txt', wxdata)

    time.sleep(30)
    return


def readws(socklist):
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
            extractobs(obsdata)
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


if __name__ == '__main__':
    scriptname = os.path.basename(__file__)
    print('started')
    # create logger with 'spam_application'
    my_logger = get_logger("main")
    my_logger.debug("a debug message")
    my_logger.setLevel(logging.DEBUG)

# """
#    logging.basicConfig(level=logging.DEBUG,
#                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
#                        datefmt="%Y-%m-%d %H:%M:%S",
#                        filename=logfile.txt
#                        )
#    logger = logging.getLogger(__name__)
# """

    my_logger.info('Logging level set ')
    if not notify.enabled():
        # Then it's probably not running is systemd with watchdog enabled
        raise Exception("Watchdog not enabled")

    # Report a status message
    notify.status("Initialising my service...")
    # time.sleep(3)

    p = configargparse.ArgParser(
        default_config_files=['/etc/default/tempest.conf', '~/.my_tempest'])
    p.add('--tempest_ID', required=False,  help='tempest station ID')
    p.add('-l', '--log_level', default='WARNING',
          choices=['DEBUG', 'INFO', 'WARNING',
                   'ERROR', 'CRITICAL'],
          help='Log level for script')

    options = p.parse_args()
    print(options)
    # logging.basicConfig(level=options.log_level)
    my_logger.setLevel(options.log_level)

    my_logger.debug('Logging level seems to be')
    my_logger.info('Logging level seems to be')
    my_logger.warning('Logging level seems to be')

    notify.ready()
    notify.status("startingloop for udp requesters...")
    # time.sleep(3)

    socklist = connectudp()

    while True:
        try:
            readws(socklist)
            # logging.debug('read loop...')
        except Exception:
            my_logger.error('An error occurred', exc_info=True)
            exit(1)
