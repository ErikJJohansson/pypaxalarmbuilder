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


# open up template csv
# maybe use template xml for each alarm type?

# write array of alarm messages to template csv file

# Poke PLC for P_AIn, P_AIChan, P_AInDual, P_AInMulti
# make sure it works for program scope tags

# Each datatype has alarms, write those alarms to spreadsheet based on tag name

# alarm group is name of PLC?


# Poke PLC for L_ModuleSts and make alarms for those modules


# get names of each sheet in workbook and put in list
def get_sheet_names(excel_book):
    sheet_list = []

    # PlantPAX AOI's have an _ for second character
    for sheet in excel_book.sheetnames:
        sheet_list.append(sheet)

    return sheet_list

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

    
    '''
    # open excel file

    # filename check
    print('Opening ' + template_excelfile)
    try:
        book = openpyxl.load_workbook(template_excelfile,keep_vba=False,keep_links=True)

    except:
        print('Unable to open excel file ' + template_excelfile)
        plc.close()
        exit()
    
    print('Opened file named ' + template_excelfile)

    sheet_name = 'Messages'

    for msg in msg_list:
        book[sheet_name].append(msg)

    # add plc name to file and save to new file
    outfile = plc_name + '_FTAE_Config.' + 'xml'
    print('Finished reading from ' + plc_name + ' PLC.')
    print('Saving to file ' + outfile)
    book.save(outfile)
    print('file saved to ' + outfile)

    plc.close()
    book.close()

    '''

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



    # Create the XML tree
    tree = ET.ElementTree(FTAE_XML_ROOT)

    # add plc name to file and save to new file
    outfile = plc_name + '_FTAE_Config.' + 'xml'
    # Write the XML tree to a file with UTF-16 encoding
    tree.write(outfile, encoding="utf-16", xml_declaration=True,short_empty_elements=False)

    plc.close()


if __name__ == "__main__":
    main()