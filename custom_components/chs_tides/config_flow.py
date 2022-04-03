"""Config flow for the Canadian Hydrographic Service (CHS) Water Level Web Services integration."""

import voluptuous as vol
import aiohttp
import logging
import re

from pychs import CHS_IWLS

from homeassistant import config_entries
from homeassistant.helpers import config_validations as cv
from homeassistant.helpers import aiohttp_client
from homeassistant.const import (
    CONF_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SCAN_INTERVAL,
    CONF_UNIT_OF_MEASUREMENT,
)

from .const import (    
    DOMAIN,
    CONF_LANGUAGE,
    CONF_STATION_CODE,
    DEFAULT_LANGUAGE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_UNIT_OF_MEASUREMENT,
)

LOGGER = logging.getLogger(__name__)

async def validate_input(data):
    """Validate input"""
    name = data.get(CONF_NAME)
    station_code = data.get(CONF_STATION_CODE)
    latitude = data.get(CONF_LATITUDE)
    longitude = data.get(CONF_LONGITUDE)
    scan_interval = data.get(CONF_SCAN_INTERVAL)
    unit_of_measurement = data.get(CONF_UNIT_OF_MEASUREMENT)
    language = data.get(CONF_LANGUAGE)

    if station_code:
        chs_iwls = CHS_IWLS(
            station_code = station_code
        )
        station_data = await chs_iwls.stations()
    elif latitude and longitude:
        chs_iwls = CHS_IWLS(
            coordinates = (data.get(CONF_LATITUDE),data.get(CONF_LONGITUDE))
        )
        station_data = await chs_iwls.station_metadata()

    if station_code is None:
        station_code = chs_iwls.station_code

    if name is None:
        name = chs_iwls.station_name

    coordinates = chs_iwls.coordinates
    latitude = re.split(",",chs_iwls.coordinates)[0])
    longitude = re.split(",",chs_iwls.coordinates)[1])

    return {
        CONF_NAME: name,
        CONF_STATION_CODE: station_code,
        CONF_LATITUDE: latitude,
        CONF_LONGITUDE: longitude,
    }

class IWLSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Canadian Hydrographic Service (CHS) Water Level Web Services"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step"""

        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(user_input)
            except aiohttp.ClientConnectionError:
                errors["base"] = "cannot_connect"

        if not errors:
            user_input[CONF_NAME] = info[CONF_NAME]
            user_input[CONF_STATION_CODE] = info[CONF_STATION_CODE]
            user_input[CONF_LATITUDE] = info[CONF_LATITUDE]
            user_input[CONF_LONGITUDE] = info[CONF_LONGITUDE]

            return self.async_create_entry(title=info[CONF_NAME], data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME): str,
                vol.Optional(CONF_STATION_CODE): str,
                vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): cv.longitude,
                vol.Required(CONF_SCAN_INTERVAL, default=60): int,
                vol.Required(CONF_UNIT_OF_MEASUREMENT, default="Feet"): vol.In(
                    ["Feet", "Meter"]                        
                ),
                vol.Required(CONF_LANGUAGE, default="English"): vol.In(
                    ["English", "French"]
                ),
            }
        )

        return self.async_show_form(
            step_id = "user", data_schema=data_schema, errors=errors
        )


