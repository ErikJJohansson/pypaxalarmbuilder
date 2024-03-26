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
    "L_ModuleSts":{
        "Alarms":{
            "ModuleFaulted": {
                "Type": "Tag",
                "Msg": 'Module fault.',
                "Params":{},
                "Cmd": ""
            },
        },
    },
    "P_AIChan": {
        "Alarms":{
            "Fail":{
                "Type": "Embedded",
                "Msg":'Channel Input bad or uncertain.  Val_InpRaw=/*S:0%Tag1*/; Val=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_InpRaw","Tag2":".Val"},
                "Cmd": "DisplayQuick "
            },
        },
    },  
    "P_AIn": {
        "Alarms":{
            "Fail":{
                "Type": "Embedded",
                "Msg": 'Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "
            },
            "HiHi":{
                "Type": "Embedded",
                "Msg": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "
            },
            "Hi":{
                "Type": "Embedded",
                "Msg": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "Lo":{
                "Type": "Embedded",
                "Msg": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "LoLo":{
                "Type": "Embedded",
                "Msg": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "Simulated":{
                "Type": "Tag",
                "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
                "Params":{"Tag1":".Sts_SubstPV"},
                "Cmd": "DisplayQuick "                
            }
        },        
    },
    "P_AInDual": {
        "Alarms":{
            "Fail":{
                "Type": "Embedded",
                "Msg": 'Analog Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "HiHi":{
                "Type": "Embedded",
                "Msg": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "Hi":{
                "Type": "Embedded",
                "Msg": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "Lo":{
                "Type": "Embedded",
                "Msg": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "LoLo":{
                "Type": "Embedded",
                "Msg": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val"},
                "Cmd": "DisplayQuick "                
            },
            "Diff":{
                "Type": "Embedded",
                "Msg": 'PVA and PVB Differential Limit Exceeded; Val_Diff=/*N:5 %Tag1 NOFILL DP:0*/',
                "Params":{"Tag1":".Val_Diff"},
                "Cmd": "DisplayQuick "                
            },
            "NoneGood":{
                "Type": "Embedded",
                "Msg": 'PVA and PVB Both Bad Quality;  Val_PVA=/*N:5 %Tag1 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag2 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val_PVA","Tag2":".Val_PVB"},
                "Cmd": "DisplayQuick "                
            },
            "OneGood":{
                "Type": "Embedded",
                "Msg": 'PVA and PVB One Bad Quality;  Val_PVA=/*N:5 %Tag1 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag2 NOFILL DP:1*/;',
                "Params":{"Tag1":".Val_PVA","Tag2":".Val_PVB"},
                "Cmd": "DisplayQuick "                
            },
            "Simulated":{
                "Type": "Tag",
                "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
                "Params":{"Tag1":".Val_PVA","Tag2":".Val_PVB"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    "P_AOut": {
        "Alarms":{
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_ValveMO': {
        "Alarms":{
            "ActuatorFault":{
                "Type": "Embedded",
                "Msg": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
                "Params":{"Tag1":".Val_Fault"},
                "Cmd": "DisplayQuick "                
            },
            "FullStall":{
                "Type": "Embedded",
                "Msg": 'Full Stall - Valve did not move',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "TransitStall":{
                "Type": "Embedded",
                "Msg": 'Transit Stall - Valve did not move to target position',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_ValveC': {
        "Alarms":{
            "ActuatorFault":{
                "Type": "Embedded",
                "Msg": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
                "Params":{"Tag1":".Val_Fault"},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_ValveSO': {
        "Alarms":{
            "FullStall":{
                "Type": "Embedded",
                "Msg": 'Full Stall - Valve did not move',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "TransitStall":{
                "Type": "Embedded",
                "Msg": 'Transit Stall - Valve did not move to target position',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_DIn': {
        "Alarms":{
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "TgtDisagree":{
                "Type": "Embedded",
                "Msg": 'Target Disagree - PV Does Not Match Target;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Inp_PV","Tag2":".Inp_Target"},
                "Cmd": "DisplayQuick "                
            },
            "Simulated":{
                "Type": "Tag",
                "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
                "Params":{"Tag1":".Sts_SubstPV"},
                "Cmd": "DisplayQuick "
            },
        },
    },
    'P_DOut': {
        "Alarms":{
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "OffFail":{
                "Type": "Embedded",
                "Msg": 'Device feedback does not confirm the device is OFF within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_Cmd","Tag2":".Val_Fdbk"},
                "Cmd": "DisplayQuick "                
            },
            "OnFail":{
                "Type": "Embedded",
                "Msg": 'Device feedback does not confirm the device is ON within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_Cmd","Tag2":".Val_Fdbk"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_PIDE': {
        "Alarms":{
            "Fail":{
                "Type": "Embedded",
                "Msg": 'PIDE instruction has a fault.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/; Val_Fault=/*S:0%Tag3*/;',
                "Params":{"Tag1":".Val_PV","Tag2":".Val_SP","Tag3":".Val_Fault"},
                "Cmd": "DisplayQuick "                
            },
            "HiHiDev":{
                "Type": "Embedded",
                "Msg": 'High-high deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
                "Cmd": "DisplayQuick "                
            },
            "HiDev":{
                "Type": "Embedded",
                "Msg": 'High deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
                "Cmd": "DisplayQuick "                
            },
            "LoDev":{
                "Type": "Embedded",
                "Msg": 'Low deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
                "Cmd": "DisplayQuick "                
            },
            "LoLoDev":{
                "Type": "Embedded",
                "Msg": 'Low-low deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
                "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_Motor': {
        "Alarms":{
            "FailToStart":{
                "Type": "Embedded",
                "Msg": 'Fail to start',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "FailToStop":{
                "Type": "Embedded",
                "Msg": 'Fail to stop',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_PF755': {
        "Alarms":{
            "DriveFault":{
                "Type": "Embedded",
                "Msg": 'Drive Fault',
                "Params":{},
                "Cmd": "DisplayQuick "
            },
            "FailToStart":{
                "Type": "Embedded",
                "Msg": 'Fail to start',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "FailToStop":{
                "Type": "Embedded",
                "Msg": 'Fail to stop',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_VSD': {
        "Alarms":{
            "DriveFault":{
                "Type": "Embedded",
                "Msg": 'Drive Fault',
                "Params":{},
                "Cmd": "DisplayQuick "
            },
            "FailToStart":{
                "Type": "Embedded",
                "Msg": 'Fail to start',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "FailToStop":{
                "Type": "Embedded",
                "Msg": 'Fail to stop',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IOFault":{
                "Type": "Embedded",
                "Msg": 'IO Fault',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    'P_LLS': {
        "Alarms":{
            "CantStart":{
                "Type": "Embedded",
                "Msg": 'Cannot start. No motors available to start',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "CantStop":{
                "Type": "Embedded",
                "Msg": 'Cannot stop. No motors available to stop',
                "Params":{},
                "Cmd": "DisplayQuick "                
            },
            "IntlkTrip":{
                "Type": "Embedded",
                "Msg": 'Interlock Trip - %Tag1',
                "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
                "Cmd": "DisplayQuick "                
            },
            "Bypassed":{
                "Type": "Tag",
                "Msg": 'Permissive & Interlock are being bypassed.',
                "Params":{"Tag1":".Sts_BypActive"},
                "Cmd": "DisplayQuick "                
            },
        },
    },
    "P_Alarm": {
        "Alarms": {
            "Alm":{
                "Type": "P_Alarm",
                "Msg": 'Alarm Active',
                "Params":{},
                "Cmd": "DisplayQuick "
            },
        },
    },
}


# These tags are always in a P_Alarm AOI
P_ALARM_TAGS = ['Com_AE.1','Com_AE.4','Com_AE.5','Com_AE.7','Com_AE.8','Com_AE.10','Com_AE.11','Cfg_MaxShelfT']