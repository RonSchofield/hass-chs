""" Binary Sensor for the Canadian Hydrographic Service (CHS) Water Level Web Services integration."""

from html import entities
import logging

from homeassistant.components.binary.sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entries: AddEntitiesCallback):

    """Set up the CHS binary sensor based on a config entry"""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        CHSBinarySensor(coordinator, entry.entry_id)
    ]

    async_add_entities(entities)

class CHSBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Defines a CHS Rising / Falling Binary sensor"""

    def __init__(
        self
        ):

        super().__init__()

    @property
    def is_on(self):
        """Return the status of the sensor"""


