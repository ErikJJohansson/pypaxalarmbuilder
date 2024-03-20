import xml.etree.ElementTree as ET

XML_VERSION = "12.1.0"

# Define namespaces
XML_NS_MAP = {
    None: "urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd",
    "dt": "urn:schemas-microsoft-com:datatypes",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# Create the root element with the defined namespaces and attributes
XML_ROOT = ET.Element("FTAeAlarmStore", attrib={
    "xmlns:dt": XML_NS_MAP["dt"],
    "xmlns": XML_NS_MAP[None],
    "xmlns:xsi": XML_NS_MAP["xsi"]#,
    #"xsi:schemaLocation": "urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd FTLDDAlarms.xsd"
})


POLL_GROUPS = ["0.10", "0.25", "0.50", "1","2","5","10","20","30","60","120"]

DEFAULT_POLL_INDEX = 4 # 2 seconds

SHELVE_MAX_VALUE = 480

DETECTOR_COMMAND = "FTAeDetectorCommand"

# Define AOI configuration and messages

AOI_CONFIG = {
    "P_AIChan": {
        "Alarms":{
            "Fail": 'Channel Input bad or uncertain.  Val_InpRaw=/*S:0%Tag1*/; Val=/*S:0%Tag2*/;'
        },
        "Msg_Params":{"Tag1":"Val_InpRaw","Tag2":"Val"},
    },
    "P_AIn": {
        "Alarms":{
            "Fail": 'Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "HiHi": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Hi": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Lo": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "LoLo": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;'
        },
        "Msg_Params":{"Tag1":"Val","Tag2":"Inp_PV"},
        
    },
    "P_AInDual": {
        "Alarms":{
            "Fail": 'Analog Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "HiHi": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Hi": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Lo": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "LoLo": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Diff": 'PVA and PVB Differential Limit Exceeded; Val_Diff=/*N:5 %Tag3 NOFILL DP:0*/',
            "NoneGood": 'PVA and PVB Both Bad Quality;  Val_PVA=/*N:5 %Tag3 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag4 NOFILL DP:1*/;',
            "OneGood": 'PVA and PVB One Bad Quality;  Val_PVA=/*N:5 %Tag3 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag4 NOFILL DP:1*/;'
        },
        "Msg_Params":{"Tag1":"Val","Tag2":"Val_Diff","Tag3":"Val_PVA","Tag4":"Val_PVB"},
    },
    "P_AOut": {
        "Alarms":{
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{},
    },
    'P_ValveMO': {
        "Alarms":{
            "ActuatorFault": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
            "FullStall": 'Full Stall - Valve did not move',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
            "TransitStall": 'Transit Stall - Valve did not move to target position',
        },
        "Msg_Params":{"Tag1":"Val_Fault"},
    },
    'P_ValveC': {
        "Alarms":{
            "ActuatorFault": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{"Tag1":"Val_Fault"},
    },
    'P_ValveSO': {
        "Alarms":{
            "FullStall": 'Full Stall - Valve did not move',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
            "TransitStall": 'Transit Stall - Valve did not move to target position',
        },
        "Msg_Params":{},
    },
    'P_DIn': {
        "Alarms":{
            "IOFault": 'IO Fault',
            "TgtDisagree": 'Target Disagree - PV Does Not Match Target;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/;'
        },
        "Msg_Params":{"Tag1":"Inp_PV","Tag2":"Inp_Target"},
    },
    'P_DOut': {
        "Alarms":{
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
            "OffFail": 'Device feedback does not confirm the device is OFF within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;',
            "OnFail": 'Device feedback does not confirm the device is ON within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;'
        },
        "Msg_Params":{"Tag1":"Val_Cmd","Tag2":"Val_Fdbk"},
    },
    'P_PIDE': {
        "Alarms":{
            "Fail": 'PIDE instruction has a fault.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/; Val_Fault=/*S:0%Tag3*/;',
            "HiDev": 'High deviation alarm.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "HiHiDev": 'High-high deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "IntlkTrip": 'Interlock Trip',
            "LoDev": 'Low deviation alarm.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "LoLoDev": 'Low-Low Deviation Alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;'
        },
        "Msg_Params":{"Tag1":"Val_PV","Tag2":"Val_SP","Tag3":"Val_Fault"},
    },
    'P_Motor': {
        "Alarms":{
            "FailToStart": 'Fail to start',
            "FailToStop": 'Fail to stop',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{},
    },
    'P_PF755': {
        "Alarms":{
            "DriveFault": 'Drive Fault',
            "FailToStart": 'Fail to start',
            "FailToStop": 'Fail to stop',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{},
    },
    'P_VSD': {
        "Alarms":{
            "DriveFault": 'Drive Fault',
            "FailToStart": 'Fail to start',
            "FailToStop": 'Fail to stop',
            "IOFault": 'IO Fault',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{},
    },
    'P_LLS': {
        "Alarms":{
            "CantStart": 'Cannot start. No motors available to start',
            "CantStop": 'Cannot stop. No motors available to stop',
            "IntlkTrip": 'Interlock Trip',
        },
        "Msg_Params":{},
    },
    "P_Alarm": {
        "Alarms": {
            '': 'In Alarm'
        },
        "Msg_Params":{}
    },
}


# These tags are always in a P_Alarm AOI
P_ALARM_TAGS = ['Com_AE.1','Com_AE.4','Com_AE.5','Com_AE.7','Com_AE.8','Com_AE.10','Com_AE.11','Cfg_MaxShelfT']