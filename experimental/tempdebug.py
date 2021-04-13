#import urllib
#import sd_notify
import logging
import collections
import configargparse
import json
import csv
import time
from websocket import create_connection
#from pint import UnitRegistry
logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )
logger = logging.getLogger(__name__)
# notify = sd_notify.Notifier()

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

def connectws():

    logging.info('Opening Websocket connection...')

    ws = create_connection(
        'wss://ws.weatherflow.com/swd/data?api_key=' + options.personal_token)
    result = ws.recv()
    #print("Received '%s'" % result)
    #print('')


    logging.debug('Listening... ')
    ws.send('{"type":"listen_start",' + ' "device_id":' +
        options.tempest_ID + ',' + ' "id":"Tempest"}')
    result = ws.recv()
    logging.debug("Received '%s'" % result)
    print('')
    return ws


def readws(ws):

    data = dict()

    logging.debug('Receiving Tempest data...')
    result = ws.recv()
    #print("Received '%s'" % result)
    print('')
    #jstring = convertJSONStringToSequence(result)
    weatherJSON = json.JSONDecoder().decode(result)
    logging.debug(weatherJSON)
    obsdata = weatherJSON['obs'][0]
    #obsdata = csv.reader(weatherJSON['obs'])

    #print(weatherJSON['summary']['feels_like'])
    #print(obsdata[0])

    data['dateTime'] = obsdata[0]
    windAvgms = obsdata[2]
    data['windSpeed'] = windAvgms * 2.23694    # convertit
    windGustms = obsdata[3]
    data['windGust'] = windGustms * 2.23694  # convertit
    data['windDir'] = obsdata[4]
    windSampInt = obsdata[5]
    AirPressure = obsdata[6]
    airTempC = obsdata[7]
    data['outTemp'] = (airTempC * 9 / 5) + 32
    data['outHumidity'] = obsdata[8]
    illumlux = obsdata[9]
    ultravil = obsdata[10]
    solarRad = obsdata[11]
    rainAccum = obsdata[12]
    data['hourRain'] = 0.0393701 * rainAccum
    precipType = obsdata[13]
    # 0=none, 1=rain, 2=hail
    lightnDistkm = obsdata[14]
    lightnCount = obsdata[15]
    battVolt = obsdata[16]
    reportIntm = obsdata[17]
    dailyRainAccum = obsdata[18]
    data['dayRain'] = 0.0393701 * dailyRainAccum
    rainAccumFinal = obsdata[19]
    rainDailyAccumFinal = obsdata[20]
    data['rain24'] = 0.0393701 * dailyRainAccum
    precipAnalType = obsdata[21]

# Actual atmospheric pressure in hPa
    aap = AirPressure * 1.0
    # Actual temperature in Celsius
    atc = airTempC
    # Temp in Kelvin K
    atk = atc + 273.15
    # Height above sea level m
    hasl = 168.479
    # gravity m/s
    grav = 9.80665
    # gasconst ait  J/(kg K)
    gasconst = 287.053
    # Temp lapse rate near sea level (<11000m) K/m
    tLapse = -0.0065
    atLapse = 0.0065
    # standard Sea Level Temp K
    slTemp = 288.15
    # standard Sea Level Pres mb
    slPres = 1013.25
    constsexp = grav/(gasconst*atLapse)
    constsinv = (gasconst*tLapse)/grav
    # constsexp

    # Adjusted-to-the-sea barometric pressure
    #a2ts = aap + ((aap * grav * hasl)/(gasconst * (atk + (hasl/400))))
    a2tsx = aap * (1 + ((atLapse * hasl) / (atk + atLapse * hasl)))**constsexp
    a2ts = 1.0 * (aap * ((1 + (((slPres/aap)**constsinv) * ((atLapse * hasl)/slTemp)))**constsexp))
    logging.debug('aap {} slp/aap {} atla {} form {} atk {:3.2f} a2ts {:4.1f} a2tsx {:4.1f} humidity {}'.format(
     aap, ((slPres/aap)**constsinv), ((atLapse * hasl)/slTemp), (((slPres/aap)**constsinv) * ((tLapse * hasl)/slTemp)),  atk, a2ts, a2tsx, data['outHumidity']))
    data['barometer'] = a2ts
# in standard places (hasl from 100-800 m, temperature from -10 to 35)
# is the coeficient something close to hasl/10, meaning simply
# a2ts is about  aap + hasl/10


    logging.debug('data time {} aap {} atc {} atk {:3.2f} a2ts {:4.1f} humidity {}'.format(
        data['dateTime'], aap, atc, atk, a2ts, data['outHumidity']))

    #print(weatherJSON['summary']['feels_like'])
    write_data('wxnow2.txt', data)
#        print(json.dumps(policies_list_id, indent=2), file=f)
#        filename = open("/tmp/wxnow2.txt", "w")

#    close(filename)
    # ws.close()
    logging.debug(' sleep...')
    time.sleep(90)
    return

if __name__ == '__main__':


    #if not notify.enabled():
    ## Then it's probably not running is systemd with watchdog enabled
    #    raise Exception("Watchdog not enabled")

    ## Report a status message
    #notify.status("Initialising my service...")
    #time.sleep(3)

    p = configargparse.ArgParser(default_config_files=['/etc/default/tempest.conf', '~/.my_tempest'])
    p.add('--tempest_ID', required=True,  help='nempest station ID')
    p.add('--personal_token', required=True, help='tempest station ID')
    p.add('-l', '--log_level', default='INFO',
               choices=['DEBUG', 'INFO', 'WARNING',
                        'ERROR', 'CRITICAL'],
               help='Log level for script')
    options = p.parse_args()
    print(options)
    log_level = getattr(logging, options.log_level.upper())
    print(log_level)
    logger.setLevel(log_level)
    #notify.ready()
    #notify.status("startingloop for web requesters...")
    #time.sleep(3)

    ws = connectws()

    while True:
        try:
            readws(ws)
        except Exception:
            logger.error('An error occurred', exc_info=True)
            exit(1)
