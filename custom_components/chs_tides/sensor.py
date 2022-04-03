"""
Canadian Hydrographic Service (CHS) Water Level Web Services.

For more details about this platform, please refer to the documentation at
https://github.com/RonSchofield/hass-cms/blob/master/README.md
"""

import logging
from datetime import timedelta, timezone, datetime as dt
from pychs import CHS_IWLS
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME,
    CONF_ID,
    CONF_SCAN_INTERVAL,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_OFFSET
)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

__version__ = '2.0.0'

CONF_ID = 'station_id'
CONF_NAME = 'name'

DEFAULT_NAME = 'CHS Tide Sensor'

SCAN_INTERVAL = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID, default="00490"): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default="m"): cv.string,
    vol.Optional(CONF_OFFSET, default=0): cv.positive_int,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the CHS Tide sensor."""
    station_id = config.get(CONF_ID)
    name = config.get(CONF_NAME, DEFAULT_NAME)
    uom = config.get(CONF_UNIT_OF_MEASUREMENT)
    scan_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    add_entities([CHSTideSensor(station_id, name, uom, scan_interval)], True)


class CHSTideSensor(Entity):
    """Representation of a CHS Tide sensor."""

    def __init__(self, station_id, name, uom, scan_interval):
        """Initialize CHS Tide sensor."""
        self._state = None
        self.station_id = station_id
        self._name = name
        self.uom = uom
        self._icon = 'mdi:sine-wave'
        self._scan_interval = scan_interval
        self._state_attributes = {}
        self._state_attributes['uom'] = uom
        #try to catch error
        self.prediction = CHS_IWLS(self.station_id)
        self.data = {}
        self.next_event_dt = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._state_attributes

    def update(self):
        """Get the tide information"""
        minute_hand = dt.utcnow().minute  
        if (self._state == None):
            _LOGGER.debug("Initialization")
            # Get the high low data 
            self.update_hilo()
            # Get the station name
            self._state_attributes['station_name'] = self.prediction.stationName
            # Get the 15 minute water levels
            self.data['wl15'] = self.prediction.water_level()
            self.set_wl15_state_attributes(quarter_round(minute_hand))
        else:
            quartersList = [15,30,45]
            if (minute_hand == 0):
                # At the top of the hour, get the new 15 minute water levels
                _LOGGER.debug("Top of the hour")
                self.data['wl15'] = self.prediction.water_level()
                self.set_wl15_state_attributes()
            elif (minute_hand in quartersList):
                # If at the quarter, update the tide level
                _LOGGER.debug("Quarter")
                self.set_wl15_state_attributes(minute_hand)
        
        # Check for the tide event (low or high)
        if(dt.utcnow() > self.next_event_dt):
            _LOGGER.debug("Next event has occured")
            self.update_hilo()

    def update_hilo(self):
        high_low = self.prediction.high_low()
        self._state = high_low['status']
        self._state_attributes['state'] = self._state
        self._state_attributes['previous_hilo_event'] = high_low['previous']['event']
        self._state_attributes['previous_hilo_height'] = self.uom_height(high_low['previous']['height'])
        self._state_attributes['previous_hilo_date'] = dt.strftime(utc_to_local(dt.strptime(high_low['previous']['date'],"%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S")
        self._state_attributes['next_hilo_event'] = high_low['next']['event']
        self._state_attributes['next_hilo_height'] = self.uom_height(high_low['next']['height'])
        self._state_attributes['next_hilo_date'] = dt.strftime(utc_to_local(dt.strptime(high_low['next']['date'],"%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S")
        self.data['hilo'] = high_low
        self.next_event_dt = dt.strptime(high_low['next']['date'],"%Y-%m-%d %H:%M:%S")

    def set_wl15_state_attributes(self, minute_hand=0):
        index = "{:02d}".format(minute_hand)
        self._state_attributes['current_height'] = self.uom_height(self.data['wl15'][index]['height'])
        self._state_attributes['current_height_as_of'] = dt.strftime(utc_to_local(dt.strptime(self.data['wl15'][index]['date'],"%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S")

    def uom_height(self, height):
        if (self.uom == 'ft'):
            return "{:.1f}".format(float(height) * 3.28084)
        else:
            return height


def quarter_round(x):
    #return 15 * round(x/15)
    return x - (x % 15)

def event_list(event_id=0, clear=False, lst=[]):
    lst.append(event_id)
    lst = list(set(lst))
    if clear:
        lst.clear()
    return lst

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

"""
def hilo_tide_event_handler(goal_team_id, goal_event_id, hass):
    team_id = str(goal_team_id)
    event_id = str(goal_event_id)
    # If the event hasn't yet been fired for this goal, fire it.
    # Else, add the event to the list anyway, in case the list is new.
    if event_list() != [0] and \
            event_id not in event_list():
        hass.bus.fire('nhl_goal', {"team_id": team_id})
        event_list(event_id)
    else:
        event_list(event_id)
"""