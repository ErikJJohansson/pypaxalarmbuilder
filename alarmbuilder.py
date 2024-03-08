from pycomm3 import LogixDriver
from sys import argv
import openpyxl
from tqdm import trange, tqdm
from itertools import product
import argparse


# Input parameters, PLC IP address, Device Shortcut (/::[Pilot]) etc.

# static list of alarm messages, this gets written into messages sheet
msg_list = ['',
            'TEST ALARM NEEDS TAG;  Val=/*N:5 %Tag1 NOFILL DP:1*/;'

]


# open up template csv
# maybe use template xml for each alarm type?

# write array of alarm messages to template csv file

# Poke PLC for P_AIn, P_AIChan, P_AInDual, P_AInMulti
# make sure it works for program scope tags

# Each datatype has alarms, write those alarms to spreadsheet based on tag name

# alarm group is name of PLC?


# Poke PLC for L_ModuleSts and make alarms for those modules

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

    # if the shortcut was left blank, create it
    if device_shortcut == '':
        device_shortcut = '/::[' + plc_name + ']'

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