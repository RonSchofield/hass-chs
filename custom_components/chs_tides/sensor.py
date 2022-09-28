"""Sensor for the Canadian Hydrographic Service (CHS) Water Level Web Services integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SCAN_INTERVAL,
    CONF_UNIT_OF_MEASUREMENT,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import (
    HomeAssistantType,
    ConfigType,
    DiscoveryInfoType,
)

from .const import (
    DOMAIN,
    CONF_LANGUAGE,
    CONF_STATION_CODE,
    DEFAULT_LANGUAGE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_UNIT_OF_MEASUREMENT,
    ATTR_HHWMT,
    ATTR_HWL,
    ATTR_HAT,
    ATTR_LLWLT,
    ATTR_HHWLT,
    ATTR_HRWL,
    ATTR_LRWL,
    ATTR_MWL,
    ATTR_LWL,
    ATTR_LAT,
    ATTR_LLWMT,
    ATTR_GLCMM,
    ATTR_NTHWL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform (
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entries: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:

class CHSSensor(SensorEntity):
    """Representation of a Canadian Hydrographic Service (CHS) Sensor"""

    def __init__(self) -> None:
        super().__init__()
