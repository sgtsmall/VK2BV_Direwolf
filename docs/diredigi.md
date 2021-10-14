
# Direwolf config

## Position Beacons
  Generally the position of the station that is broadcasting including Location, messages, telemtry,...

#### Position Report beacon defaults to RF 0

`PBEACON delay=6:00 every=15:00 overlay=S SYMBOL="weather station" lat-36^27.04s long=146^26.12E COMMENTCMD="tail -l /tmp/wxnow.txt"`

#### Position Report beacon to IG

`PBEACON sendto=IG delay=6:00 every=15:00 overlay=S SYMBOL="weather station" lat-36^27.04s long=146^26.12E COMMENTCMD="tail -l /tmp/wxnow.txt"`


## Object Beacon
  Locations and information about static objects relevant to the location.
- If the object is already reported on APRS-IS don't send it to IG, however could be useful to send information over local RF.
- If the object is not in APRS-IS then send to IG

#### Object Report beacon defaults to RF 0

`OBEACON OBJNAME=VK3RNU LAT=36^27.08S LONG=146^48.18E SYMBOL=/r
FREQ=438.525 OFFSET=-5.000 TONE=0.0 COMMENT=”Mt Stanley”`

## IGate rules (APRS-IS)

#### Server side filter
  `IGFILTER t/mw/VK3MS-2/50 p/NTE/NCY`

- Limit the data that will be retrieved from the Igate Server
- Processed as default AND Rule
  - `t/mw/VK3MS-2/50` - type Messages and weather from APRS-IS within 50km of station
  - `p/NTE/NCY` - Any type that starts with 'NTE' or 'NCY'



#### IGTXVIA - send data from Igate to RF

- `IGTXVIA 0 WIDE1-1,WIDE2-1`   - send as general packet
- `IGTXVIA 0 VK3xxx`     - send to particular digipeater
- `IGTXVIA 0`    - send without packet header to avoid digipeating [Recommended]



#### IGTXLIMIT - Manage quantity of messages that can be sent.


- `IGTXLIMIT 4 8` - (4 packets in a minute, 8 packets in 5 minutes)

## Filter Rules - Client
 These work slightly differently within Direwolf with some more processing ligic available.

- `FILTER IG 0` Filter from IG to radio
  - Not needed if using IGFILTER
  - Could be used to send different IG messages via different radios
- `FILTER 0 IG` Filter from radio to IG
- `FILTER 0 0` filter from radio to radio


- `FILTER 0 0 `
  - `! d/*` - Fillin digi - only digi if not heard from a digipeater
  - `r/lat/lon/range` - decimal degrees and km
  - `b/VK3MS*/VK3XX*` - all packets from buddies
  - `g/VK3MS*/VK2PSF*/VK3BV*` - all messages from one of these stations
- `FILTER 0 0 ( ! d/* ) & ( r/-36.450/146.435/50 | b/VK3MS*/VK3XX* | g/VK3MS*/VK2PSF*/VK3BV*)`

### Recommended Links about source data and server side filter

[WXSVR-AU APRS Weather Server for Australia][e31280c1]

  [e31280c1]: http://mckserver-aw.mmckernan.id.au/wxsvr-au/index.php "AU Weather SERVER"

[Filter Rules for APRS-IS][203c4a3f]

  [203c4a3f]: http://www.aprs-is.net/javaprsfilter.aspx "Filter Rules"


[Using APRSICE for for APRS-IS filter test][7c9ff106]

  [7c9ff106]: https://groups.io/g/APRSISCE/topic/34600041 "APRSICE filter test"

## Digipeat rules
  Create rules to manage the Repeating of Information over RF
- Digipeat rules act on the channel and the address
- Try to only repeat information that something else doesn't cover.
- Keep information relevant to the service area.
- Try to minimise repeating bad records.

#### Digipeat Rule From RF 0 to RF 0  
  `DIGIPEAT 0 0 ^WIDE[3-7]-[1-7]$ ^WIDE[12]-[12]$ TRACE`

##### Fields:

  - From 0
  - To 0
  - Aliases `^WIDE[3-7]-[1-7]$` - e.g. WIDE3-5 is treated as WIDE1-1
  - Wide `^WIDE[12]-[12]$` Patterns we want t treat properly e.g. WIDE2-1 will become WIDE2-*
  -  Premptive Digipeat
    - `TRACE` - show the path
    - `OFF` - Not digipeated
    - `DROP` - Hide History - [do not use]
    - `MARK` - Adjust path - [do not use]


Example

```
#Device Information
#Channel Information
IGSERVER xxxxxxxx
IGLOGIN xxxxxxxx




#Position Report beacon
PBEACON delay=3:00 every=15:00 overlay=S SYMBOL="weather station" lat-36^27.04s long=146^26.12E COMMENTCMD="tail -l /tmp/wxnow.txt"

PBEACON delay=4:00 every=15:00 overlay=S SYMBOL="Digi" lat-36^27.04s long=146^26.12E COMMENT=" Radio XXX"


#Position Report beacon to IG

PBEACON sendto=IG delay=5:00 every=15:00 overlay=S SYMBOL="weather station" lat-36^27.04s long=146^26.12E COMMENTCMD="tail -l /tmp/wxnow.txt"

PBEACON sendto=IG delay=6:00 every=15:00 overlay=S SYMBOL="Digi" lat-36^27.04s long=146^26.12E COMMENT=" Radio XXX"
#Object Beacon

OBEACON OBJNAME=VK3RNU LAT=36^27.08S LONG=146^48.18E SYMBOL=/r FREQ=438.525 OFFSET=-5.000 TONE=0.0 COMMENT=”Mt Stanley”

#IGate rules (APRS-IS)

# Server side filter
IGFILTER t/mw/VK3MS-2/50 p/NTE/NCY

# IGTXVIA - send data from Igate to RF

IGTXVIA 0

# IGTXLIMIT - Manage quantity of messages that can be sent.

IGTXLIMIT 4 8

# Filter Rules - Client
FILTER 0 0 ( ! d/* ) & ( r/-36.450/146.435/50 | b/VK3MS*/VK3XX* | g/VK3MS*/VK2PSF*/VK3BV*)

#Digipeat rules
DIGIPEAT 0 0 ^WIDE[3-7]-[1-7]$ ^WIDE[12]-[12]$ TRACE
```
