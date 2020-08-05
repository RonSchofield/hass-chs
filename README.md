# hass-chs
Canadian Hydrographic Service Water Levels integration into Home Assistant

## Integration into Home Assistant
1. Create **custom_components** folder in the **config** directory.
2. Download and extract the files from github.
3. Copy the folders and files inside the **custom_components** folder to the **custom_components** folder in Home Assistant.
4.  Add the sensor to the **configuration.yaml** file.
   
        sensor:
          - platform: chs_tides

5. The default tide station is Halifax, NS. If you wish to use another station in Canada. Look at **stations.md**  file and add the line

            station_id: <id>

    replacing the id with one from the table. You must use leading zeros.

6. Restart the Home Assistant server.