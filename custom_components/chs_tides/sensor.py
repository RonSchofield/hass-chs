"""
Canadian Hydrographic Service (CHS) Water Level Web Services.

For more details about this platform, please refer to the documentation at
https://github.com/RonSchofield/hass-cms/blob/master/README.md
"""

import logging
from datetime import timedelta, datetime as dt
from pychs import Predictions
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_ID, CONF_SCAN_INTERVAL, CONF_UNIT_OF_MEASUREMENT, CONF_OFFSET)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

__version__ = '0.0.1'

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
    scan_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    add_entities([CHSTideSensor(station_id, name, scan_interval)], True)


class CHSTideSensor(Entity):
    """Representation of a CHS Tide sensor."""

    def __init__(self, station_id, name, scan_interval):
        """Initialize CHS Tide sensor."""
        self._state = None
        self.station_id = station_id
        self._name = name
        self._icon = 'mdi:current-ac'
        self._scan_interval = scan_interval
        self._state_attributes = {}

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
        prediction = Predictions(self.station_id)
        if (self._state == None):
            high_low = prediction.high_low()
            self._state = high_low['status']


def event_list(event_id=0, clear=False, lst=[]):
    lst.append(event_id)
    lst = list(set(lst))
    if clear:
        lst.clear()
    return lst

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