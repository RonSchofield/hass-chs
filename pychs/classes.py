"""
Python wrapper for Canadian Hydrographic Service (CHS) Water Level Web Services
"""

from zeep import Client
from datetime import datetime, timedelta

OBSERVATIONS_BASE = "https://ws-shc.qc.dfo-mpo.gc.ca/observations/"
PREDICTIONS_BASE = "https://ws-shc.qc.dfo-mpo.gc.ca/predictions/"

class Observations:
    """

    Attributes
    ----------
    station_id : int
        The Station ID of the Site

    Methods
    -------
    water_level()
        Water level in meters
    water_salinity()
        Water salinity in parts per thousand (0/00)
    water_temperature()
        Water temperature in Celcius degree
    atmospheric_pressure()
        Atmospheric pressure in millibars

    """

class Predictions:
    """
    
    Attributes
    ----------
    station_id : int
        The Station ID of the Site
    start_date : datetime
        The start date
    end_date : datetime
        The end date  

    Methods
    -------
    high_low()
        Water levels of high and low tides
    water_level()
        Water Levels each 15 minutes ( :00, :15, :30 and :45 )
    next_high()
        Water levels and time of the next high tide
    next_low()
        Water levels and time of the next low tide

    """

