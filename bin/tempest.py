#import urllib
import sd_notify
import collections
import configargparse
import json
import csv
import time
from websocket import create_connection
#from pint import UnitRegistry

notify = sd_notify.Notifier()


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
#
# def getURLasJSONSequence(url):
#    s = getURLasString(url)
#    return convertJSONStringToSequence(s)

# url = "http://127.0.0.1:8081/lookupnames" # my local web service
#s = getURLasString(url)
# print s
#j = getURLasJSONSequence(url)
# print j

#sampleJSON = [{"LastName": "DaVinci", "FirstName": "Leonardo"}, {"LastName": "Newton", "FirstName": "Isaac"}]

#filteredList = [e["FirstName"] for e in sampleJSON if e["LastName"].startswith("D")]
# print filteredList


def Connectandread():

    data = dict()
    #print('Opening Websocket connection...')


    ws = create_connection(
        'wss://ws.weatherflow.com/swd/data?api_key=' + personal_token)
    result = ws.recv()
    #print("Received '%s'" % result)
    #print('')


    print('Listening... ', end = '')
    ws.send('{"type":"listen_start",' + ' "device_id":' +
        tempest_ID + ',' + ' "id":"Tempest"}')
    result = ws.recv()
    #print("Received '%s'" % result)
    #print('')

    #print('Receiving Tempest data...')
    result = ws.recv()
    #print("Received '%s'" % result)
    #print('')
    #jstring = convertJSONStringToSequence(result)
    weatherJSON = json.JSONDecoder().decode(result)
    #print(weatherJSON['obs'])
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
    data['barometer'] = obsdata[6]
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


    print('data time {} press {} temp {} humidity {}'.format(
        data['dateTime'], data['barometer'], airTempC, data['outHumidity']), end = '')
    #print(weatherJSON['summary']['feels_like'])
    filename = open("/tmp/wxnow.txt", "w")
    write_data('/tmp/wxnow.txt', data)
    ws.close()
    print(' sleep...')
    time.sleep(300)
    return

if __name__ == '__main__':

    if not notify.enabled():
    # Then it's probably not running is systemd with watchdog enabled
        raise Exception("Watchdog not enabled")

    # Report a status message
    notify.status("Initialising my service...")
    time.sleep(3)

    p = configargparse.ArgParser(default_config_files=['/etc/default/tempest.conf', '~/.my_tempest'])
    p.add('--tempest_ID', required=True,  help='nempest station ID')
    p.add('--personal_token', required=True, help='tempest station ID')

    options = p.parse_args()

    notify.ready()
    notify.status("startingloop for web requesters...")
    time.sleep(3)

    while True:
        Connectandread()
