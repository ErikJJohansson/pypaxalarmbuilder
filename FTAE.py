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

SIMULATED_SEVERITY = 101
BYPASSED_SEVERITY = 101
MODFAULT_SEVERITY = 501

# Alarms are repeated across many AOI's
ALARM_DEFINITIONS = {
    "Bypassed":{
        "Type": "Tag",
        "Msg": 'Permissive and interlock are being bypassed.',
        "Params":{},
        "Severity": str(BYPASSED_SEVERITY),
        "DataItem": "TAGPATH.Sts_BypActive",              
    },
    "Simulated":{
        "Name": "PLCNAME_TAGNAME_Alm_Simulated",
        "Type": "Tag",
        "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
        "Params":{},
        "Cmd": "AE_DisplayQuick TAGPATH PROGPATH",
        "Severity": str(SIMULATED_SEVERITY),
        "DataItem": "TAGPATH.Sts_SubstPV",                   
    },
}





# Define AOI configuration and messages

AOI_CONFIG = {
    "L_ModuleSts":{
        "ModuleFaulted": {
            "Type": "Tag",
            "Msg": "Module is in faulted state",
            "Params": {},
            "Name": "PLCNAME_TAGNAME_Alm_ModuleFaulted",
            "Severity": str(MODFAULT_SEVERITY),
            "DataItem": "TAGPATH.Sts_IOFault",
        }
    },
    "P_AIChan": {
        "Fail":{
            "Name": "PLCNAME_TAGNAME_Alm_Fail",
            "Type": "Embedded",
            "Msg":'Channel Input bad or uncertain.  Val_InpRaw=/*S:0%Tag1*/; Val=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_InpRaw","Tag2":".Val"},
            "Severity": "TAGPATH.Cfg_FailSeverity",
            "DataItem": "TAGPATH.Alm_Fail",
        }
    },
    "P_AIn": 
    {
        "Fail":{
            "Name": "PLCNAME_TAGNAME_Alm_Fail",
            "Type": "Embedded",
            "Msg": 'Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_FailSeverity",
            "DataItem": "TAGPATH.Alm_Fail",
        },
        "HiHi":{
            "Name": "PLCNAME_TAGNAME_Alm_HiHi",
            "Type": "Embedded",
            "Msg": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_HiHiSeverity",
            "DataItem": "TAGPATH.Alm_HiHi",
        },
        "Hi":{
            "Name": "PLCNAME_TAGNAME_Alm_Hi",
            "Type": "Embedded",
            "Msg": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_HiSeverity",
            "DataItem": "TAGPATH.Alm_Hi",          
        },
        "Lo":{
            "Name": "PLCNAME_TAGNAME_Alm_Lo",
            "Type": "Embedded",
            "Msg": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_LoSeverity",
            "DataItem": "TAGPATH.Alm_Lo",               
        },
        "LoLo":{
            "Name": "PLCNAME_TAGNAME_Alm_LoLo",
            "Type": "Embedded",
            "Msg": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_LoLoSeverity",
            "DataItem": "TAGPATH.Alm_LoLo",                   
        },
        "Simulated":{
            "Name": "PLCNAME_TAGNAME_Alm_Simulated",
            "Type": "Tag",
            "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
            "Params":{},
            "Severity": str(SIMULATED_SEVERITY),
            "DataItem": "TAGPATH.Sts_SubstPV",                 
        }    
    },
    "P_AInDual": {
        "Fail":{
            "Name": "PLCNAME_TAGNAME_Alm_Fail",
            "Type": "Embedded",
            "Msg": 'Input bad or uncertain.  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_FailSeverity",
            "DataItem": "TAGPATH.Alm_Fail",
        },
        "HiHi":{
            "Name": "PLCNAME_TAGNAME_Alm_HiHi",
            "Type": "Embedded",
            "Msg": 'High-High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_HiHiSeverity",
            "DataItem": "TAGPATH.Alm_HiHi",
        },
        "Hi":{
            "Name": "PLCNAME_TAGNAME_Alm_Hi",
            "Type": "Embedded",
            "Msg": 'High Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_HiSeverity",
            "DataItem": "TAGPATH.Alm_Hi",           
        },
        "Lo":{
            "Name": "PLCNAME_TAGNAME_Alm_Lo",
            "Type": "Embedded",
            "Msg": 'Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_LoSeverity",
            "DataItem": "TAGPATH.Alm_Lo",               
        },
        "LoLo":{
            "Name": "PLCNAME_TAGNAME_Alm_LoLo",
            "Type": "Embedded",
            "Msg": 'Low-Low Alarm;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val"},
            "Severity": "TAGPATH.Cfg_LoLoSeverity",
            "DataItem": "TAGPATH.Alm_LoLo",                    
        },
        "Simulated":{
            "Name": "PLCNAME_TAGNAME_Alm_Simulated",
            "Type": "Tag",
            "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
            "Params":{},
            "Severity": str(SIMULATED_SEVERITY),
            "DataItem": "TAGPATH.Sts_SubstPV",                
        },
        "Diff":{
            "Name": "PLCNAME_TAGNAME_Alm_LoLo",
            "Type": "Embedded",
            "Msg": 'PVA and PVB Differential Limit Exceeded; Val_Diff=/*N:5 %Tag1 NOFILL DP:0*/',
            "Params":{"Tag1":".Val_Diff"},
            "Severity": "TAGPATH.Cfg_LoLoSeverity",
            "DataItem": "TAGPATH.Alm_LoLo",                   
        },
        "NoneGood":{
            "Name": "PLCNAME_TAGNAME_Alm_NoneGood",
            "Type": "Embedded",
            "Msg": 'PVA and PVB Both Bad Quality;  Val_PVA=/*N:5 %Tag1 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag2 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val_PVA","Tag2":".Val_PVB"},
            "Severity": "TAGPATH.Cfg_NoneGoodSeverity",
            "DataItem": "TAGPATH.Alm_NoneGood",                               
        },
        "OneGood":{
            "Name": "PLCNAME_TAGNAME_Alm_OneGood",
            "Type": "Embedded",
            "Msg": 'PVA and PVB One Bad Quality;  Val_PVA=/*N:5 %Tag1 NOFILL DP:1*/; Val_PVB=/*N:5 %Tag2 NOFILL DP:1*/;',
            "Params":{"Tag1":".Val_PVA","Tag2":".Val_PVB"},
            "Severity": "TAGPATH.Cfg_OneGoodSeverity",
            "DataItem": "TAGPATH.Alm_OneGood",                  
        },
        "Simulated":{
            "Name": "PLCNAME_TAGNAME_Alm_Simulated",
            "Type": "Tag",
            "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
            "Params":{},
            "Cmd": "AE_DisplayQuick TAGPATH PROGPATH",
            "Severity": str(SIMULATED_SEVERITY),
            "DataItem": "TAGPATH.Sts_SubstPV",                   
        },
    },
    "P_AOut": {
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_ValveMO': {
        "ActuatorFault":{
            "Type": "Embedded",
            "Msg": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
            "Params":{"Tag1":".Val_Fault"},
            "Severity": "TAGPATH.Cfg_ActuatorFaultSeverity",
            "DataItem": "TAGPATH.Alm_ActuatorFault",             
        },
        "FullStall":{
            "Type": "Embedded",
            "Msg": 'Full Stall - Valve did not move',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FullStallSeverity",
            "DataItem": "TAGPATH.Alm_FullStall",               
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },              
        "TransitStall":{
            "Type": "Embedded",
            "Msg": 'Transit Stall - Valve did not move to target position',
            "Params":{},
            "Severity": "TAGPATH.Cfg_TransitStallSeverity",
            "DataItem": "TAGPATH.Alm_TransitStall",               
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_ValveC': {
        "ActuatorFault":{
            "Type": "Embedded",
            "Msg": 'Actuator fault.  Val_Fault=/*S:0%Tag1*/;',
            "Params":{"Tag1":".Val_Fault"},
            "Severity": "TAGPATH.Cfg_ActuatorFaultSeverity",
            "DataItem": "TAGPATH.Alm_ActuatorFault",             
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        }, 
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_ValveSO': {
        "FullStall":{
            "Type": "Embedded",
            "Msg": 'Full Stall - Valve did not move',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FullStallSeverity",
            "DataItem": "TAGPATH.Alm_FullStall",               
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "TransitStall":{
            "Type": "Embedded",
            "Msg": 'Transit Stall - Valve did not move to target position',
            "Params":{},
            "Severity": "TAGPATH.Cfg_TransitStallSeverity",
            "DataItem": "TAGPATH.Alm_TransitStall",               
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_DIn': {
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "TgtDisagree":{
            "Type": "Embedded",
            "Msg": 'Target Disagree - PV Does Not Match Target;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Inp_PV","Tag2":".Inp_Target"},
            "Severity": "TAGPATH.Cfg_TgtDisagreeSeverity",
            "DataItem": "TAGPATH.Alm_TgtDisagree",                 
        },
        "Simulated":{
            "Name": "PLCNAME_TAGNAME_Alm_Simulated",
            "Type": "Tag",
            "Msg": 'Input is being simulated. This can defeat interlocks and safety systems.',
            "Params":{},
            "Cmd": "AE_DisplayQuick TAGPATH PROGPATH",
            "Severity": str(SIMULATED_SEVERITY),
            "DataItem": "TAGPATH.Sts_SubstPV",                   
        },
    },
    'P_DOut': {
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "OffFail":{
            "Type": "Embedded",
            "Msg": 'Device feedback does not confirm the device is OFF within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_Cmd","Tag2":".Val_Fdbk"},
            "Severity": "TAGPATH.Cfg_OffFailSeverity",
            "DataItem": "TAGPATH.Alm_OffFail",              
        },
        "OnFail":{
            "Type": "Embedded",
            "Msg": 'Device feedback does not confirm the device is ON within the configured time.  Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_Cmd","Tag2":".Val_Fdbk"},
            "Severity": "TAGPATH.Cfg_OnFailSeverity",
            "DataItem": "TAGPATH.Alm_OnFail",                
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_PIDE': {
        "Fail":{
            "Type": "Embedded",
            "Msg": 'PIDE instruction has a fault.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/; Val_Fault=/*S:0%Tag3*/;',
            "Params":{"Tag1":".Val_PV","Tag2":".Val_SP","Tag3":".Val_Fault"},
            "Severity": "TAGPATH.Cfg_FailSeverity",
            "DataItem": "TAGPATH.Alm_Fail",          
        },
        "HiHiDev":{
            "Type": "Embedded",
            "Msg": 'High-high deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
            "Severity": "TAGPATH.Cfg_HiHiDevSeverity",
            "DataItem": "TAGPATH.Alm_HiHiDev",               
        },
        "HiDev":{
            "Type": "Embedded",
            "Msg": 'High deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
            "Severity": "TAGPATH.Cfg_HiDevSeverity",
            "DataItem": "TAGPATH.Alm_HiDev",                 
        },
        "LoDev":{
            "Type": "Embedded",
            "Msg": 'Low deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
            "Severity": "TAGPATH.Cfg_LoDevSeverity",
            "DataItem": "TAGPATH.Alm_LoDev",                
        },
        "LoLoDev":{
            "Type": "Embedded",
            "Msg": 'Low-low deviation alarm.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;',
            "Params":{"Tag1":".Val_PV","Tag2":".Val_SP"},
            "Severity": "TAGPATH.Cfg_LoLoDevSeverity",
            "DataItem": "TAGPATH.Alm_LoLoDev",                 
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_Motor': {
        "FailToStart":{
            "Type": "Embedded",
            "Msg": 'Fail to start',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStartSeverity",
            "DataItem": "TAGPATH.Alm_FailToStart",                
        },
        "FailToStop":{
            "Type": "Embedded",
            "Msg": 'Fail to stop',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStopSeverity",
            "DataItem": "TAGPATH.Alm_FailToStop",                
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_PF755': {
        "DriveFault":{
            "Type": "Embedded",
            "Msg": 'Drive Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_DriveFaultSeverity",
            "DataItem": "TAGPATH.Alm_DriveFault",  
        },
        "FailToStart":{
            "Type": "Embedded",
            "Msg": 'Failed to start',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStartSeverity",
            "DataItem": "TAGPATH.Alm_FailToStart",              
        },
        "FailToStop":{
            "Type": "Embedded",
            "Msg": 'Failed to stop',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStopSeverity",
            "DataItem": "TAGPATH.Alm_FailToStop",               
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_VSD': {
        "DriveFault":{
            "Type": "Embedded",
            "Msg": 'Drive Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_DriveFaultSeverity",
            "DataItem": "TAGPATH.Alm_DriveFault",  
        },
        "FailToStart":{
            "Type": "Embedded",
            "Msg": 'Failed to start',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStartSeverity",
            "DataItem": "TAGPATH.Alm_FailToStart",              
        },
        "FailToStop":{
            "Type": "Embedded",
            "Msg": 'Failed to stop',
            "Params":{},
            "Severity": "TAGPATH.Cfg_FailToStopSeverity",
            "DataItem": "TAGPATH.Alm_FailToStop",                         
        },
        "IOFault":{
            "Type": "Embedded",
            "Msg": 'IO Fault',
            "Params":{},
            "Severity": "TAGPATH.Cfg_IOFaultSeverity",
            "DataItem": "TAGPATH.Alm_IOFault",                   
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    'P_LLS': {
        "CantStart":{
            "Type": "Embedded",
            "Msg": 'Cannot start. No motors available to start',
            "Params":{},
            "Severity": "TAGPATH.Cfg_CantStartSeverity",
            "DataItem": "TAGPATH.Alm_CantStart",                 
        },
        "CantStop":{
            "Type": "Embedded",
            "Msg": 'Cannot stop. No motors available to stop',
            "Params":{},
            "Severity": "TAGPATH.Cfg_CantStopSeverity",
            "DataItem": "TAGPATH.Alm_CantStop",              
        },
        "IntlkTrip":{
            "Type": "Embedded",
            "Msg": 'Interlock Trip - /*S:20%Tag1*/',
            "Params":{"Tag1":"_Intlk.Val_FirstOutTxt"},
            "Severity": "TAGPATH.Cfg_IntlkTripSeverity",
            "DataItem": "TAGPATH.Alm_IntlkTrip",                 
        },
        "Bypassed":{
            "Type": "Tag",
            "Msg": 'Permissive and interlock are being bypassed.',
            "Params":{},
            "Severity": str(BYPASSED_SEVERITY),
            "DataItem": "TAGPATH.Sts_BypActive",              
        },
    },
    "P_Alarm": {
        "Alm":{
            "Type": "P_Alarm",
            "Msg": 'Alarm Active',
            "Params":{},
            "Severity": "TAGPATH.Cfg_Severity",
            "DataItem": "TAGPATH.Alm",  
        },
    },
}


# These tags are always in a P_Alarm AOI
P_ALARM_TAGS = ['.Com_AE.1','.Com_AE.4','.Com_AE.5','.Com_AE.7','.Com_AE.8','.Com_AE.10','.Com_AE.11','.Cfg_MaxShelfT']

ALARM_TYPE_CONFIG = {
    'Embedded': {
        "Name": "PLCNAME_TAGNAME_Alm_ALMNAME",
        "Cmd": "AE_DisplayQuick TAGPATH PROGPATH",
        "DisabledDataItem": "TAGPATH.ALMTAG.Com_AE.9",
        "AckedDataItem": "TAGPATH.ALMTAG.Com_AE.1",
        "SuppressedDataItem": "TAGPATH.ALMTAG.Com_AE.6",
        "ShelvedDataItem": "TAGPATH.ALMTAG.Com_AE.3",
        "RemoteAckAllDataItem": "TAGPATH.ALMTAG.Com_AE.1",
        "RemoteDisableDataItem": "TAGPATH.ALMTAG.Com_AE.10",
        "RemoteEnableDataItem": "TAGPATH.ALMTAG.Com_AE.11",
        "RemoteSuppressDataItem": "TAGPATH.ALMTAG.Com_AE.7",
        "RemoteUnSuppressDataItem": "TAGPATH.ALMTAG.Com_AE.8",
        "RemoteShelveAllDataItem": "TAGPATH.ALMTAG.Com_AE.4",
        "RemoteUnShelveDataItem": "TAGPATH.ALMTAG.Com_AE.5",
        "RemoteShelveDuration": "TAGPATH.ALMTAG.Cfg_MaxShelfT",
    },
    'P_Alarm': {
        "Name": "PLCNAME_TAGNAME_Alm",
        "Cmd": "AE_DisplayP_AlarmFaceplate TAGPATH PROGPATH TAGPATH.Cfg_Cond",
        "DisabledDataItem": "TAGPATH.Com_AE.9",
        "AckedDataItem": "TAGPATH.Com_AE.1",
        "SuppressedDataItem": "TAGPATH.Com_AE.6",
        "ShelvedDataItem": "TAGPATH.Com_AE.3",
        "RemoteAckAllDataItem": "TAGPATH.Com_AE.1",
        "RemoteDisableDataItem": "TAGPATH.Com_AE.10",
        "RemoteEnableDataItem": "TAGPATH.Com_AE.11",
        "RemoteSuppressDataItem": "TAGPATH.Com_AE.7",
        "RemoteUnSuppressDataItem": "TAGPATH.Com_AE.8",
        "RemoteShelveAllDataItem": "TAGPATH.Com_AE.4",
        "RemoteUnShelveDataItem": "TAGPATH.Com_AE.5",
        "RemoteShelveDuration": "TAGPATH.Cfg_MaxShelfT",
    },
    "Tag": {
        "Name": "PLCNAME_TAGNAME_Alm_ALMNAME",
        "Cmd": "AE_DisplayQuick TAGPATH PROGPATH",
        "DisabledDataItem": "",
        "AckedDataItem": "",
        "SuppressedDataItem": "",
        "ShelvedDataItem": "",
        "RemoteAckAllDataItem": "",
        "RemoteDisableDataItem": "",
        "RemoteEnableDataItem": "",
        "RemoteSuppressDataItem": "",
        "RemoteUnSuppressDataItem": "",
        "RemoteShelveAllDataItem": "",
        "RemoteUnShelveDataItem": "",
        "RemoteShelveDuration": "",
    }  
}


