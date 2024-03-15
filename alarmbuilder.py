from pycomm3 import LogixDriver
from sys import argv
import openpyxl
from tqdm import trange, tqdm
from itertools import product
import argparse
import xml.etree.ElementTree as ET

# Input parameters, PLC IP address, Device Shortcut (/::[Pilot]) etc.

# static list of alarm messages, this gets written into messages sheet
FTAE_MSG_LIST = ['',
            'TEST ALARM NEEDS TAG;  Val=/*N:5 %Tag1 NOFILL DP:1*/;',
            'WOOOOO'
]

FTAE_XML_VERSION = "12.1.0"

# Define namespaces
FTAE_XML_NS_MAP = {
    None: "urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd",
    "dt": "urn:schemas-microsoft-com:datatypes",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}

# Create the root element with the defined namespaces and attributes
FTAE_XML_ROOT = ET.Element("FTAeAlarmStore", attrib={
    "xmlns:dt": FTAE_XML_NS_MAP["dt"],
    "xmlns": FTAE_XML_NS_MAP[None],
    "xmlns:xsi": FTAE_XML_NS_MAP["xsi"],
    "xsi:schemaLocation": "urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd FTLDDAlarms.xsd"
})

FTAE_DETECTOR_COMMAND = "FTAeDetectorCommand"

FTAE_GROUP_ID = 1   # hardcoded for now, will change to use input

FTAE_SHELVE_MAX_VALUE = 480

# Define AOI tags and their respective update rates 
FTAE_AOI_ALARMS = {
    'P_AIn': ["Fail","HiHi","Hi","Lo","LoLo"],
    'P_AIChan': ["Fail"],
    'P_ValveSO': ["IOFault","IntlkTrip","OffFail","OnFail"],
    'P_DIn': ["IOFault","TgtDisagree"],

}  

FTAE_AOI_PARAMS = {
    "P_AIn": {"Tag1":"Val"},
    "P_AIChan": {"Tag1":"Val"},
    "P_ValveSO": {"Tag1":"Val"},
    "P_DIn": {"Tag1":"Val"}
}


# These tags are always in a P_Alarm AOI
FTAE_P_ALARM_TAGS = ['Com_AE.1','Com_AE.4','Com_AE.5','Com_AE.7','Com_AE.8','Com_AE.10','Com_AE.11','Cfg_MaxShelfT']

# open up template csv
# maybe use template xml for each alarm type?

# write array of alarm messages to template csv file

# Poke PLC for P_AIn, P_AIChan, P_AInDual, P_AInMulti
# make sure it works for program scope tags

# Each datatype has alarms, write those alarms to spreadsheet based on tag name

# alarm group is name of PLC?


# Poke PLC for L_ModuleSts and make alarms for those modules

# make a  function so its easier to read
def write_alarm(ET,parent,aoi_type,aoi_instance,alarm_tag,device_shortcut, group_id,message_id,param_list):
    alarmelement = ET.SubElement(parent, "FTAlarmElement", attrib={"name": aoi_instance + '_Alm_' + alarm_tag,"inuse":"Yes","latched":"false","ackRequired":"true","style":"Discrete"})
    alarmelement.tail = "\n"

    discreteelement = ET.SubElement(alarmelement, "DiscreteElement")
    discreteelement.tail = "\n"

    dataitem = ET.SubElement(discreteelement, "DataItem")
    dataitem.text = device_shortcut + aoi_instance + '_Alm_' + alarm_tag
    dataitem.tail = "\n"

    style = ET.SubElement(discreteelement, "Style")
    style.text = "DiscreteTrue"
    style.tail = "\n"

    severity = ET.SubElement(discreteelement, "Severity")
    severity.text = device_shortcut + aoi_instance + '.Cfg_' + alarm_tag + 'Severity'
    severity.tail = "\n"

    delayinterval   = ET.SubElement(discreteelement, "DelayInterval")
    delayinterval.text = "0"
    delayinterval.tail = "\n"

    enabletag = ET.SubElement(discreteelement, "EnableTag")
    enabletag.text = "false"
    enabletag.tail = "\n"

    userdata = ET.SubElement(discreteelement, "UserData")
    userdata.tail = "\n"

    rsvcmd = ET.SubElement(discreteelement, "RSVCmd")
    rsvcmd.text = "AE_DisplayQuick " + device_shortcut + aoi_instance + " " + device_shortcut
    rsvcmd.tail = "\n"

    alarmclass = ET.SubElement(discreteelement, "AlarmClass")
    alarmclass.text = aoi_type
    alarmclass.tail = "\n"

    groupid = ET.SubElement(discreteelement, "GroupID")
    groupid.text = str(group_id)
    groupid.tail = "\n"

    handshaketags = ET.SubElement(discreteelement, "HandshakeTags")
    handshaketags.tail = "\n"

    inalarmdataitem = ET.SubElement(handshaketags, "InAlarmDataItem")
    inalarmdataitem.tail = "\n"

    disableddataitem = ET.SubElement(handshaketags, "DisabledDataItem")
    disableddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.9'
    disableddataitem.tail = "\n"

    ackeddataitem = ET.SubElement(handshaketags, "AckedDataItem")
    ackeddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.1'
    ackeddataitem.tail = "\n"

    suppresseddataitem = ET.SubElement(handshaketags, "SuppressedDataItem")
    suppresseddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.6'
    suppresseddataitem.tail = "\n"

    shelveddataitem = ET.SubElement(handshaketags, "ShelvedDataItem")
    shelveddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.3'
    shelveddataitem.tail = "\n"

    # Add RemoteAckAllDataItem element
    remoteAckAllDataItem = ET.SubElement(discreteelement, "RemoteAckAllDataItem", AutoReset="false")
    remoteAckAllDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.1'
    remoteAckAllDataItem.tail = '\n'

    # Add RemoteDisableDataItem element
    remoteDisableDataItem = ET.SubElement(discreteelement, "RemoteDisableDataItem", AutoReset="true")
    remoteDisableDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.10'
    remoteDisableDataItem.tail = '\n'

    # Add RemoteEnableDataItem element
    remoteEnableDataItem = ET.SubElement(discreteelement, "RemoteEnableDataItem", AutoReset="true")
    remoteEnableDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.11'
    remoteEnableDataItem.tail = '\n'

    # Add RemoteSuppressDataItem element
    remoteSuppressDataItem = ET.SubElement(discreteelement, "RemoteSuppressDataItem", AutoReset="true")
    remoteSuppressDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.7'
    remoteSuppressDataItem.tail = '\n'

    # Add RemoteUnSuppressDataItem element
    remoteUnsuppressDataItem = ET.SubElement(discreteelement, "RemoteUnSuppressDataItem", AutoReset="true")
    remoteUnsuppressDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.8'
    remoteUnsuppressDataItem.tail = '\n'

    # Add RemoteShelveAllDataItem element
    remoteShelveAllDataItem = ET.SubElement(discreteelement, "RemoteShelveAllDataItem", AutoReset="true")
    remoteShelveAllDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.4'
    remoteShelveAllDataItem.tail = '\n'

    # Add RemoteUnShelveDataItem element
    remoteUnshelveDataItem = ET.SubElement(discreteelement, "RemoteUnShelveDataItem", AutoReset="true")
    remoteUnshelveDataItem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.5'
    remoteUnshelveDataItem.tail = '\n'

    # Add RemoteShelveDuration element
    remoteShelveDuration = ET.SubElement(discreteelement, "RemoteShelveDuration")
    remoteShelveDuration.text = device_shortcut + aoi_instance + '.' + alarm_tag + ".Cfg_MaxShelfT"
    remoteShelveDuration.tail = '\n'

    # Add MessageID element
    messageID = ET.SubElement(discreteelement, "MessageID")
    messageID.text = str(message_id)
    messageID.tail = '\n'

    parameters = ET.SubElement(discreteelement, "Params")
    parameters.tail = "\n"

    # Add parameters to the alarm
    for param_name in param_list.keys():
        param = ET.SubElement(parameters, "Param", attrib={"key": param_name})
        param.text = device_shortcut + aoi_instance + '.' + param_list[param_name]
        param.tail = "\n"

# get names of each sheet in workbook and put in list
def get_sheet_names(excel_book):
    sheet_list = []

    # PlantPAX AOI's have an _ for second character
    for sheet in excel_book.sheetnames:
        sheet_list.append(sheet)

    return sheet_list

def get_aoi_tag_instances(plc, tag_type):
    """
    function returns list of tag names matching struct type
    """
    #return tag_list

    tag_list = []

    for tag, _def in plc.tags.items():
        if _def['data_type_name'] == tag_type and not(_def['alias']):
            if _def['dim'] > 0:
                tag_list = tag_list + get_dim_list(tag,_def['dimensions'])
            else:
                tag_list.append(tag)

    return tag_list

def get_dim_list(base_tag, dim_list):
    '''
    function takes a list which has the array size and turns it into a list with all iterations
    '''
    # remove 0's
    filtered_list = list(filter(lambda num: num != 0, dim_list))

    temp = []

    for indices in product(*[range(dim) for dim in filtered_list]):
        temp.append(base_tag + ''.join(f'[{i}]' for i in indices))

    return temp

# append elements to instance of tag
def make_tag_list(base_tag,sub_tags):
    '''
    returns the full tag path of a given base tag and sub tags
    '''
    # concatenate base tag
    read_list = [base_tag + '.' + s for s in sub_tags]

    return read_list

def main():

    # default filename of template file included in the repo
    template_excelfile = 'FTAE_AlarmExport.xlsx'
    
    # will be replaced with PLC name
    default_deviceshortcut = ''

    # Parse arguments
   
    parser = argparse.ArgumentParser(
        description='Python-based PlantPAX alarm builder tool',
        epilog='This tool works on both Windows and Mac.')
    
    # Add command-line arguments
    parser.add_argument('commpath', help='Path to PLC')
    parser.add_argument('deviceshortcut', nargs='?', default=default_deviceshortcut,help='Shortcut in FTView')
                                       
    args = parser.parse_args()

    # Access the parsed arguments
    commpath = args.commpath
    device_shortcut = args.deviceshortcut

    # open connection to PLC

    plc = LogixDriver(commpath, init_tags=True,init_program_tags=True)

    print('Connecting to PLC.')
    try:
        plc.open()
        plc_name = plc.get_plc_name()

        print('Connected to ' + plc_name + ' PLC at ' + commpath)
    except:
        print('Unable to connect to PLC at ' + commpath)
        exit()

    # if the shortcut was left blank, create it and spit out a default message
    if device_shortcut == '':
        device_shortcut = '/::[' + plc_name + ']'

        print('No FTView device shortcut specified. Using PLC name. Path is: ' + device_shortcut)
    
    # create version element and append it to the root
    version = ET.SubElement(FTAE_XML_ROOT, "Version")
    version.text = FTAE_XML_VERSION
    version.tail = "\n"

    # Create a commands element and append it to the root
    commands = ET.SubElement(FTAE_XML_ROOT, "Commands")
    commands.tail = "\n"

    # Create a FTAeDetectorCommand element and append it to the commands, hardcoded for now
    setlanguages_command = ET.SubElement(commands, FTAE_DETECTOR_COMMAND)
    setlanguages_command.tail = "\n"

    setlanguages_operation = ET.SubElement(setlanguages_command, "Operation")
    setlanguages_operation.text = "SetLanguages"
    setlanguages_operation.tail = "\n"

    setlanguages_params = ET.SubElement(setlanguages_command, "Language", attrib={"xml:lang": "en-US"})
    setlanguages_params.tail = "\n"

    # set poll groups
    setdapollgroups_command = ET.SubElement(commands, FTAE_DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE_XML_VERSION})
    setdapollgroups_command.tail = "\n"
    setdapollgroups_operation = ET.SubElement(setdapollgroups_command, "Operation")
    setdapollgroups_operation.text = "SetDAPollGroups"
    setdapollgroups_operation.tail = "\n"

    # Hardcoded
    FTAE_POLL_GROUPS = ["0.10", "0.25", "0.50", "1","2","5","10","20","30","60","120"]

    pollgroups = ET.SubElement(setdapollgroups_command, "PollGroups")
    pollgroups.tail = "\n"

    # store pollgroup rates in list, access by index when wanting to add tags
    pollgrouptags_rate =[]
    for i,rate in enumerate(FTAE_POLL_GROUPS):
        pollgrouptags_rate.append(ET.SubElement(pollgroups, "PollGroupTags", attrib={"rate": rate}))
        pollgrouptags_rate[i].tail = "\n"

    # write message structure
    writemsgs_command = ET.SubElement(commands, FTAE_DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE_XML_VERSION})
    writemsgs_command.tail = "\n"
    writemsgs_operation = ET.SubElement(writemsgs_command, "Operation")
    writemsgs_operation.text = "WriteMsg"
    writemsgs_operation.tail = "\n"

    messages = ET.SubElement(writemsgs_command, "Messages")
    messages.tail = "\n"

    # loop through list of messages and write to xml
    for i,msg in enumerate(FTAE_MSG_LIST):
        
        # skip first element
        # honestly wtf rockwell what is this structure
        if i > 0:
            message = ET.SubElement(messages, "Message", attrib={"id": str(i)})
            message.tail = "\n"
            msgs = ET.SubElement(message, "Msgs")
            msgs.tail = "\n"
            msg_txt = ET.SubElement(msgs, "Msg", attrib={"xml:lang": "en-US"})
            msg_txt.text = msg
            msg_txt.tail = "\n"

    # write alarm groups structure
    writealarmgroups_command = ET.SubElement(commands, FTAE_DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE_XML_VERSION})
    writealarmgroups_command.tail = "\n"
    writealarmgroups_operation = ET.SubElement(writealarmgroups_command, "Operation")
    writealarmgroups_operation.text = "WriteAlarmGroups"

    alarmgroups = ET.SubElement(writealarmgroups_command, "Groups")
    alarmgroups.tail = "\n"

    alarmgroup = ET.SubElement(alarmgroups, "Group", attrib={"id": str(FTAE_GROUP_ID),"parentID":"0"}) # maybe pass an input? requres user to know what group they are in
    alarmgroup.text = plc_name
    alarmgroup.tail = "\n"

    # structure for alarms
    writeconfig_command = ET.SubElement(commands, FTAE_DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE_XML_VERSION})
    writeconfig_command.tail = "\n"
    writeconfig_operation = ET.SubElement(writeconfig_command, "Operation")
    writeconfig_operation.text = "WriteConfig"
    writeconfig_operation.tail = "\n"

    # this becomes the "root" of where all the alarms are stored
    alarmelements = ET.SubElement(writeconfig_command, "FTAlarmElements", attrib={"shelveMaxValue":str(FTAE_SHELVE_MAX_VALUE)})
    alarmelements.tail = "\n"

    # loop through each AOI type and write to xml
    for aoi_type in FTAE_AOI_ALARMS.keys():

        # get list of tags for each AOI typ
        aoi_instance_list = get_aoi_tag_instances(plc, aoi_type)

        # get list of alarm tags for each AOI type
        aoi_alarm_tags = FTAE_AOI_ALARMS[aoi_type]

        # loop through each instance of the AOI type
        for aoi_instance in aoi_instance_list:
            

            # loop through each alarm in list for the instance type
            for alarm_tag in aoi_alarm_tags:
                
                # ADD THE ALARM
                write_alarm(ET,alarmelements,aoi_type,aoi_instance,alarm_tag,device_shortcut,FTAE_GROUP_ID,1,FTAE_AOI_PARAMS[aoi_type])
                
                # create tag path
                alarm_tag_and_elements = make_tag_list(alarm_tag,FTAE_P_ALARM_TAGS)

                # add alarm tag to poll group
                alm_tag = ET.SubElement(pollgrouptags_rate[4],"Tag")
                alm_tag.text = device_shortcut + aoi_instance + '.Alm_' + alarm_tag
                alm_tag.tail = "\n"

                # add P_Alarm tags to poll group
                for tag_name in alarm_tag_and_elements:
                    tag = ET.SubElement(pollgrouptags_rate[4],"Tag")
                    tag.text = device_shortcut + aoi_instance + '.' + tag_name
                    tag.tail = "\n"




    # Create the XML tree
    tree = ET.ElementTree(FTAE_XML_ROOT)

    # add plc name to file and save to new file
    outfile = plc_name + '_FTAE_Config.' + 'xml'
    # Write the XML tree to a file with UTF-16 encoding
    tree.write(outfile, encoding="utf-16", xml_declaration=True,short_empty_elements=False)

    plc.close()


if __name__ == "__main__":
    main()