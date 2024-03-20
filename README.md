# pypaxalarmbuilder

## Description

This project improves on the PlantPAX Alarm builder tool by poking the PLC for all the instances of each PlantPAX AOI instantiation and generating alarms based on that.

## Motivation

The original PlantPAX alarm builder runs using VB or something.

The tool is painful and requires using an .ACD file to generate the alarms. This tool just looks at the PLC and completes in under 10 seconds. After that the generated XML file is ready to be imported into FactoryTalk Alarms & Events

## Connnecting to the PLC to generate the XML file

The tool requires a few command line arguments to work. a properly formatted command is shown below

```
alarmbuilder.py 10.10.17.10/4 [GroupID] [Device Shortcut]

```

10.10.17.10/4 is the PLC IP address and slot number of the PLC, without the slot number and just the IP address (like '10.10.17.10' it will default to slot 0)

The group ID is the base ID for the PLC. this needs to range from 1-9. The tool limits having 9 PLC's connected to a FactoryTalk Alarms & Events instance. This defaults to 1 and its used as the basis to assign the alarm group and message indexes

The device shortcut is the communications path set in the project (Typically /::[PLC_SHORTCUT])

## Other Notes

The generated XML file will be stored in the same directory the alarmbuilder.py file is run. The name will have the PLC_Name at the beginning of it followed by "_FTAE_AlarmExport.xml"

The generated file must be imported into FactoryTalk Alarms and events. you must select the "Import as XML" Option

If there is only 1 PLC connected to the FactoryTalk Alarms and Events instance, keep GroupID as 1 

The script will generate an alarm message for each AOI instance. The contents of the message will contain data from the .Cfg_Label and .Cfg_Desc tags in the PlantPAX AOI. Be sure to fill this data out before running the tool