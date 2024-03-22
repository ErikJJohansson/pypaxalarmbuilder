from pycomm3 import LogixDriver
from sys import argv
import argparse
import xml.etree.ElementTree as ET
import re
import FTAE
import xmlschema

def validate_xml(xml_file, xsd_file):
    schema = xmlschema.XMLSchema(xsd_file)
    try:
        schema.validate(xml_file)
        print("XML is valid against XSD.")
    except xmlschema.XMLSchemaValidationError as e:
        print("XML is not valid against XSD:")
        print(e)

def replace_characters_with_underscore(input_string, characters):
    pattern = '[' + re.escape(characters) + ']'
    return re.sub(pattern, '_', input_string)

# check if tag is program tag
def get_program_name_for_tag(tag):
    # Regular expression pattern to extract "Anode_Gas_Management"
    pattern = r'Program:([^.]+)'

    # Extracting the substring
    match = re.search(pattern, tag)

    if match:
        extracted_string = match.group(1)
        return extracted_string
    else:
        return ''
    
def get_shortcut_name(device_shortcut):
    '''
    function to get the name of the device shortcut
    '''

    pattern = r'\[(.*?)\]'

    # Extracting the substring
    match = re.search(pattern, device_shortcut)

    if match:
        extracted_string = match.group(1)
        return extracted_string
    else:
        return ''

# made this to keep track of indexes for alarms and whatnot
def create_alarmgroup_database(plc_groupID, plc_name, plc_program_list):
    '''
    function to create a database of alarm groups
    
    # PLC becomes group name, ID ranges from 1 to 9, max 9 PLC's per FTAE
    # groupID for each program is X01-X99 where X is the PLC group ID
    # add groupID for program to dictionary of program names
    # add index element to each progrm name group ID
    # messages start at X0YY0000 where XX is group ID
    # YY is program number, max 99 programs per PLC

    # Controller scope tag message index starts at 101, to 9999
    # Program Scope tag message index starts at 10001, to 19999
    # Message ID can range between 1-2147483647
    '''
    alarm_dict = {}

    # index 0 is for controller scoped tags
    alarm_dict[''] = {}
    alarm_dict['']['groupID'] = str(plc_groupID)
    alarm_dict['']['msg_index'] = str(plc_groupID*10000000 + 1)
    alarm_dict['']['parentID'] = '0'
    alarm_dict['']['Name'] = plc_name

    for i, program in enumerate(plc_program_list):
        alarm_dict[program] = {}
        alarm_dict[program]['groupID'] = str((plc_groupID*100) + (i+1))
        alarm_dict[program]['msg_index'] = str((plc_groupID*10000000) + (i+1)*10000 + 1)
        alarm_dict[program]['parentID'] = str(plc_groupID)
        alarm_dict[program]['Name'] = program

    return alarm_dict

# writes alarm groups based on alarm dictionary generated
def write_alarmgroups(ET, parent, alarm_dict):

    groups = ET.SubElement(parent, "Groups")
    groups.tail = '\n'   

    for key in alarm_dict.keys():
        alarmgroup = ET.SubElement(groups, "Group", attrib={"id": alarm_dict[key]['groupID'],"parentID":alarm_dict[key]['parentID']})
        alarmgroup.text = alarm_dict[key]['Name']
        alarmgroup.tail = '\n'

def write_msg(ET,parent,msg_id,msg_text):
    message = ET.SubElement(parent, "Message", attrib={"id": str(msg_id)})
    message.tail = '\n'
    msgs = ET.SubElement(message, "Msgs")
    msgs.tail = '\n'
    msg_txt = ET.SubElement(msgs, "Msg", attrib={"xml:lang": "en-US"})
    msg_txt.text = msg_text
    msg_txt.tail = '\n'

# P_Alarm has a different structure compared to AOI's with it embedded
def write_alarm_p_alarm(ET,parent,plc_name,aoi_instance,device_shortcut, group_id, message_id):

    aoi_instance_formatted = replace_characters_with_underscore(aoi_instance,':.[]')
    alarmelementname = plc_name + '_' + aoi_instance_formatted + '_Alm'

    alarmelement = ET.SubElement(parent, "FTAlarmElement", attrib={"name": alarmelementname,"inuse":"Yes","latched":"false","ackRequired":"true","style":"Discrete"})
    alarmelement.tail = '\n'

    discreteelement = ET.SubElement(alarmelement, "DiscreteElement")
    discreteelement.tail = '\n'

    dataitem = ET.SubElement(discreteelement, "DataItem")
    dataitem.text = device_shortcut + aoi_instance + '.Alm'
    dataitem.tail = '\n'

    style = ET.SubElement(discreteelement, "Style")
    style.text = "DiscreteTrue"
    style.tail = '\n'

    severity = ET.SubElement(discreteelement, "Severity")
    severity.text = device_shortcut + aoi_instance + '.Cfg_Severity'
    severity.tail = '\n'

    delayinterval   = ET.SubElement(discreteelement, "DelayInterval")
    delayinterval.text = "0"
    delayinterval.tail = '\n'

    enabletag = ET.SubElement(discreteelement, "EnableTag")
    enabletag.text = "false"
    enabletag.tail = '\n'

    userdata = ET.SubElement(discreteelement, "UserData")
    userdata.tail = '\n'

    rsvcmd = ET.SubElement(discreteelement, "RSVCmd")
    if aoi_instance.startswith('Program:'):
        rsvcmd.text = "AE_DisplayP_AlarmFaceplate " + device_shortcut + aoi_instance + " " + device_shortcut + aoi_instance.split('.')[0] + '. ' + device_shortcut + aoi_instance + '.Cfg_Cond' 
    else:
        rsvcmd.text = "AE_DisplayP_AlarmFaceplate " + device_shortcut + aoi_instance + " " + device_shortcut + ' ' + device_shortcut + aoi_instance + '.Cfg_Cond'
        
    rsvcmd.tail = '\n'

    alarmclass = ET.SubElement(discreteelement, "AlarmClass")
    alarmclass.text = 'P_Alarm'
    alarmclass.tail = '\n'

    groupid = ET.SubElement(discreteelement, "GroupID")
    groupid.text = str(group_id)
    groupid.tail = '\n'

    handshaketags = ET.SubElement(discreteelement, "HandshakeTags")
    handshaketags.tail = '\n'

    inalarmdataitem = ET.SubElement(handshaketags, "InAlarmDataItem")
    inalarmdataitem.tail = '\n'

    disableddataitem = ET.SubElement(handshaketags, "DisabledDataItem")
    disableddataitem.text = device_shortcut + aoi_instance + '.Com_AE.9'
    disableddataitem.tail = '\n'

    ackeddataitem = ET.SubElement(handshaketags, "AckedDataItem")
    ackeddataitem.text = device_shortcut + aoi_instance + '.Com_AE.1'
    ackeddataitem.tail = '\n'

    suppresseddataitem = ET.SubElement(handshaketags, "SuppressedDataItem")
    suppresseddataitem.text = device_shortcut + aoi_instance + '.Com_AE.6'
    suppresseddataitem.tail = '\n'

    shelveddataitem = ET.SubElement(handshaketags, "ShelvedDataItem")
    shelveddataitem.text = device_shortcut + aoi_instance + '.Com_AE.3'
    shelveddataitem.tail = '\n'

    # Add RemoteAckAllDataItem element
    remoteAckAllDataItem = ET.SubElement(discreteelement, "RemoteAckAllDataItem", AutoReset="false")
    remoteAckAllDataItem.text = device_shortcut + aoi_instance + '.Com_AE.1'
    remoteAckAllDataItem.tail = '\n'

    # Add RemoteDisableDataItem element
    remoteDisableDataItem = ET.SubElement(discreteelement, "RemoteDisableDataItem", AutoReset="true")
    remoteDisableDataItem.text = device_shortcut + aoi_instance + '.Com_AE.10'
    remoteDisableDataItem.tail = '\n'

    # Add RemoteEnableDataItem element
    remoteEnableDataItem = ET.SubElement(discreteelement, "RemoteEnableDataItem", AutoReset="true")
    remoteEnableDataItem.text = device_shortcut + aoi_instance + '.Com_AE.11'
    remoteEnableDataItem.tail = '\n'

    # Add RemoteSuppressDataItem element
    remoteSuppressDataItem = ET.SubElement(discreteelement, "RemoteSuppressDataItem", AutoReset="true")
    remoteSuppressDataItem.text = device_shortcut + aoi_instance + '.Com_AE.7'
    remoteSuppressDataItem.tail = '\n'

    # Add RemoteUnSuppressDataItem element
    remoteUnsuppressDataItem = ET.SubElement(discreteelement, "RemoteUnSuppressDataItem", AutoReset="true")
    remoteUnsuppressDataItem.text = device_shortcut + aoi_instance + '.Com_AE.8'
    remoteUnsuppressDataItem.tail = '\n'

    # Add RemoteShelveAllDataItem element
    remoteShelveAllDataItem = ET.SubElement(discreteelement, "RemoteShelveAllDataItem", AutoReset="true")
    remoteShelveAllDataItem.text = device_shortcut + aoi_instance + '.Com_AE.4'
    remoteShelveAllDataItem.tail = '\n'

    # Add RemoteUnShelveDataItem element
    remoteUnshelveDataItem = ET.SubElement(discreteelement, "RemoteUnShelveDataItem", AutoReset="true")
    remoteUnshelveDataItem.text = device_shortcut + aoi_instance + '.Com_AE.5'
    remoteUnshelveDataItem.tail = '\n'

    # Add RemoteShelveDuration element
    remoteShelveDuration = ET.SubElement(discreteelement, "RemoteShelveDuration")
    remoteShelveDuration.text = device_shortcut + aoi_instance + ".Cfg_MaxShelfT"
    remoteShelveDuration.tail = '\n'

    # Add MessageID element
    messageID = ET.SubElement(discreteelement, "MessageID")
    messageID.text = str(message_id)
    messageID.tail = '\n'

    parameters = ET.SubElement(discreteelement, "Params")
    parameters.tail = '\n'

# make a  function so its easier to read
def write_alarm(ET,parent,plc_name,aoi_type,aoi_instance,alarm_tag,device_shortcut, group_id,message_id,param_list):

    aoi_instance_formatted = replace_characters_with_underscore(aoi_instance,':.[]')
    alarmelementname = plc_name + '_' + aoi_instance_formatted + '_' + alarm_tag + '_Alm'

    alarmelement = ET.SubElement(parent, "FTAlarmElement", attrib={"name": alarmelementname,"inuse":"Yes","latched":"false","ackRequired":"true","style":"Discrete"})
    alarmelement.tail = '\n'

    discreteelement = ET.SubElement(alarmelement, "DiscreteElement")
    discreteelement.tail = '\n'

    dataitem = ET.SubElement(discreteelement, "DataItem")
    dataitem.text = device_shortcut + aoi_instance + '.Alm_' + alarm_tag
    dataitem.tail = '\n'

    style = ET.SubElement(discreteelement, "Style")
    style.text = "DiscreteTrue"
    style.tail = '\n'

    severity = ET.SubElement(discreteelement, "Severity")
    severity.text = device_shortcut + aoi_instance + '.Cfg_' + alarm_tag + 'Severity'
    severity.tail = '\n'

    delayinterval   = ET.SubElement(discreteelement, "DelayInterval")
    delayinterval.text = "0"
    delayinterval.tail = '\n'

    enabletag = ET.SubElement(discreteelement, "EnableTag")
    enabletag.text = "false"
    enabletag.tail = '\n'

    userdata = ET.SubElement(discreteelement, "UserData")
    userdata.tail = '\n'

    rsvcmd = ET.SubElement(discreteelement, "RSVCmd")
    if aoi_instance.startswith('Program:'):
        rsvcmd.text = "AE_DisplayQuick " + device_shortcut + aoi_instance + " " + device_shortcut + aoi_instance.split('.')[0] + '.'
    else:
        rsvcmd.text = "AE_DisplayQuick " + device_shortcut + aoi_instance + " " + device_shortcut
        
    rsvcmd.tail = '\n'

    alarmclass = ET.SubElement(discreteelement, "AlarmClass")
    alarmclass.text = aoi_type
    alarmclass.tail = '\n'

    groupid = ET.SubElement(discreteelement, "GroupID")
    groupid.text = str(group_id)
    groupid.tail = '\n'

    handshaketags = ET.SubElement(discreteelement, "HandshakeTags")
    handshaketags.tail = '\n'

    inalarmdataitem = ET.SubElement(handshaketags, "InAlarmDataItem")
    inalarmdataitem.tail = '\n'

    disableddataitem = ET.SubElement(handshaketags, "DisabledDataItem")
    disableddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.9'
    disableddataitem.tail = '\n'

    ackeddataitem = ET.SubElement(handshaketags, "AckedDataItem")
    ackeddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.1'
    ackeddataitem.tail = '\n'

    suppresseddataitem = ET.SubElement(handshaketags, "SuppressedDataItem")
    suppresseddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.6'
    suppresseddataitem.tail = '\n'

    shelveddataitem = ET.SubElement(handshaketags, "ShelvedDataItem")
    shelveddataitem.text = device_shortcut + aoi_instance + '.' + alarm_tag + '.Com_AE.3'
    shelveddataitem.tail = '\n'

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
    parameters.tail = '\n'

    # Add parameters to the alarm
    for param_name in param_list.keys():
        param = ET.SubElement(parameters, "Param", attrib={"key": param_name})
        param.text = device_shortcut + aoi_instance + '.' + param_list[param_name]
        param.tail = '\n'



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
    
    # will be replaced with PLC name
    default_deviceshortcut = ''
    default_groupID = 1

    # Parse arguments
   
    parser = argparse.ArgumentParser(
        description='Python-based PlantPAX alarm builder tool',
        epilog='This tool works on both Windows and Mac.')
    
    # Add command-line arguments
    parser.add_argument('commpath', help='Path to PLC')
    #parser.add_argument('appname', help='FTView application name')   
    #parser.add_argument('areaname', help='FTView application area name')
    #parser.add_argument('servername', help='FTView Alarm & Event Server name')
    parser.add_argument('groupID', nargs='?', default=default_groupID,help='PLC Group ID for alarms 1-9')
    parser.add_argument('deviceshortcut', nargs='?', default=default_deviceshortcut,help='Shortcut in FTView')

                                       
    args = parser.parse_args()

    # Access the parsed arguments
    commpath = args.commpath
    #appname = args.appname
    #servername = args.servername
    device_shortcut = args.deviceshortcut
    plc_groupID = int(args.groupID)

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

    # get list of programs, this will be used to separate into different alarm groups
    plc_program_list = plc.info['programs'].keys()

    plc_shortcut_name = get_shortcut_name(device_shortcut)
    
    print('Generating alarm group database')
    # create alarm group database
    alarm_group_db = create_alarmgroup_database(plc_groupID,plc_name,plc_program_list)

    print('Generating FTAE XML file')
    # create version element and append it to the root
    version = ET.SubElement(FTAE.XML_ROOT, "Version")
    version.text = FTAE.XML_VERSION
    version.tail = '\n'

    # Create a commands element and append it to the root
    commands = ET.SubElement(FTAE.XML_ROOT, "Commands")
    commands.tail = '\n'

    # Create a FTAeDetectorCommand element and append it to the commands, hardcoded for now
    setlanguages_command = ET.SubElement(commands, FTAE.DETECTOR_COMMAND)
    setlanguages_command.tail = '\n'

    setlanguages_operation = ET.SubElement(setlanguages_command, "Operation")
    setlanguages_operation.text = "SetLanguages"
    setlanguages_operation.tail = '\n'

    setlanguages_params = ET.SubElement(setlanguages_command, "Language", attrib={"xml:lang": "en-US"})
    setlanguages_params.tail = '\n'

    # set poll groups
    setdapollgroups_command = ET.SubElement(commands, FTAE.DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE.XML_VERSION})
    setdapollgroups_command.tail = '\n'
    setdapollgroups_operation = ET.SubElement(setdapollgroups_command, "Operation")
    setdapollgroups_operation.text = "SetDAPollGroups"
    setdapollgroups_operation.tail = '\n'



    pollgroups = ET.SubElement(setdapollgroups_command, "PollGroups")
    pollgroups.tail = '\n'

    # store pollgroup rates in list, access by index when wanting to add tags
    pollgrouptags_rate =[]
    for i,rate in enumerate(FTAE.POLL_GROUPS):
        pollgrouptags_rate.append(ET.SubElement(pollgroups, "PollGroupTags", attrib={"rate": rate}))
        pollgrouptags_rate[i].tail = '\n'

    # write message structure
    writemsgs_command = ET.SubElement(commands, FTAE.DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE.XML_VERSION})
    writemsgs_command.tail = '\n'
    writemsgs_operation = ET.SubElement(writemsgs_command, "Operation")
    writemsgs_operation.text = "WriteMsg"
    writemsgs_operation.tail = '\n'

    messages = ET.SubElement(writemsgs_command, "Messages")
    messages.tail = '\n'

    # write alarm groups structure
    writealarmgroups_command = ET.SubElement(commands, FTAE.DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE.XML_VERSION})
    writealarmgroups_command.tail = '\n'
    writealarmgroups_operation = ET.SubElement(writealarmgroups_command, "Operation")
    writealarmgroups_operation.text = "WriteAlarmGroup"

    # write alarm groups to xml based on the database
    write_alarmgroups(ET,writealarmgroups_command,alarm_group_db)

    # structure for alarms
    writeconfig_command = ET.SubElement(commands, FTAE.DETECTOR_COMMAND,attrib={"style": "FTAeDefaultDetector", "version": FTAE.XML_VERSION})
    writeconfig_command.tail = '\n'
    writeconfig_operation = ET.SubElement(writeconfig_command, "Operation")
    writeconfig_operation.text = "WriteConfig"
    writeconfig_operation.tail = '\n'

    # this becomes the "root" of where all the alarms are stored
    alarmelements = ET.SubElement(writeconfig_command, "FTAlarmElements", attrib={"shelveMaxValue":str(FTAE.SHELVE_MAX_VALUE)})
    alarmelements.tail = '\n'

    #aoi_type = 'P_AIChan'
    # loop through each AOI type and write to xml
    for aoi_type in FTAE.AOI_CONFIG.keys():
        # get list of tags for each AOI typ
        aoi_instance_list = get_aoi_tag_instances(plc, aoi_type)

        # get list of alarm tags for each AOI type
        aoi_alarm_tags = FTAE.AOI_CONFIG[aoi_type]['Alarms']

        # loop through each instance of the AOI type
        for aoi_instance in aoi_instance_list:
            
            # get the P&ID tag and description from PLC
            # this is used to help make the messages for the alarms

            aoi_cfg_tag = plc.read(aoi_instance + '.Cfg_Tag')[1]
            if aoi_type == 'P_Alarm':
                aoi_cfg_desc = plc.read(aoi_instance + '.Cfg_Cond')[1]
            else:
                aoi_cfg_desc = plc.read(aoi_instance + '.Cfg_Desc')[1]

            # check if tag is program tag
            aoi_program_name = get_program_name_for_tag(aoi_instance)

            # maybe makes things easier to read
            aoi_msg_start = plc_name + ' - ' + aoi_cfg_tag + ' - ' + aoi_cfg_desc + ' - '

            # add parameters for alarm tags to tag list
            alarm_tag_parameters = make_tag_list(aoi_instance,FTAE.AOI_CONFIG[aoi_type]['Msg_Params'].values())


            for tag in alarm_tag_parameters:
                # add P_Alarm tags to poll group
                alm_tag_parameter = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                alm_tag_parameter.text = device_shortcut + tag
                alm_tag_parameter.tail = '\n'

            # loop through each alarm in list for the instance type
            if aoi_type == 'P_Alarm':
                alarm_message_index = alarm_group_db[aoi_program_name]['msg_index']
                alarm_groupID = alarm_group_db[aoi_program_name]['groupID']

                # add alarm message to messages
                write_msg(ET,messages,alarm_message_index,aoi_msg_start + FTAE.AOI_CONFIG[aoi_type]['Alarms'][''])

                # add alarm to alarms
                write_alarm_p_alarm(ET,alarmelements,plc_name,aoi_instance,device_shortcut,alarm_groupID,alarm_message_index)
                # add alarm tags to tags

                # create tag path
                alarm_tag_and_elements = make_tag_list(aoi_instance,FTAE.P_ALARM_TAGS)

                # add alarm tag to poll group
                alm_tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                alm_tag.text = device_shortcut + aoi_instance + '.Alm'
                alm_tag.tail = '\n'

                severity_tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                severity_tag.text = device_shortcut + aoi_instance + '.Cfg_' + alarm_tag + 'Severity'
                severity_tag.tail = '\n'

                # add P_Alarm tags to poll group
                for tag_name in alarm_tag_and_elements:
                    tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                    tag.text = device_shortcut + tag_name
                    tag.tail = '\n'

                # update the message index
                index_update = int(alarm_message_index) + 1
                alarm_group_db[aoi_program_name]['msg_index'] = str(index_update)

            else:
                for alarm_tag in aoi_alarm_tags:
                    
                    alarm_message_index = alarm_group_db[aoi_program_name]['msg_index']
                    alarm_groupID = alarm_group_db[aoi_program_name]['groupID']

                    # add alarm message to messages
                    write_msg(ET,messages,alarm_message_index,aoi_msg_start + FTAE.AOI_CONFIG[aoi_type]['Alarms'][alarm_tag])

                    # add alarm to alarms
                    write_alarm(ET,alarmelements,plc_name,aoi_type,aoi_instance,alarm_tag,device_shortcut,alarm_groupID,alarm_message_index,FTAE.AOI_CONFIG[aoi_type]['Msg_Params'])
                    
                    # add alarm tags to tags

                    # create tag path
                    alarm_tag_and_elements = make_tag_list(alarm_tag,FTAE.P_ALARM_TAGS)

                    # add alarm tag to poll group
                    alm_tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                    alm_tag.text = device_shortcut + aoi_instance + '.Alm_' + alarm_tag
                    alm_tag.tail = '\n'

                    severity_tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                    severity_tag.text = device_shortcut + aoi_instance + '.Cfg_' + alarm_tag + 'Severity'
                    severity_tag.tail = '\n'

                    # add P_Alarm tags to poll group
                    for tag_name in alarm_tag_and_elements:
                        tag = ET.SubElement(pollgrouptags_rate[FTAE.DEFAULT_POLL_INDEX],"Tag")
                        tag.text = device_shortcut + aoi_instance + '.' + tag_name
                        tag.tail = '\n'

                    # update the message index
                    index_update = int(alarm_message_index) + 1
                    alarm_group_db[aoi_program_name]['msg_index'] = str(index_update)

    print('Generation complete. Writing to file')
    # Create the XML tree
    tree = ET.ElementTree(FTAE.XML_ROOT)

    # add plc name to file and save to new file
    #outfile = appname + '_' + servername + '_AlarmExport.' + 'xml'
    outfile = plc_name + '_FTAE_AlarmExport.' + 'xml'
    # Write the XML tree to a file with UTF-16 encoding
    tree.write(outfile, encoding="utf-16", xml_declaration=True,short_empty_elements=False)

    plc.close()

    print('Done. File saved as ' + outfile + '.')
    print('Validating XML against XSD')
    validate_xml(outfile,'FTLDDAlarms.xsd')
    
if __name__ == "__main__":
    main()