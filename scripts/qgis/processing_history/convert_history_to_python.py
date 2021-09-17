import os
import re
import sys

if len(sys.argv) < 2:
    print("No input data dir specified - exiting")
    sys.exit(1)

data_dir = sys.argv[1]

if len(sys.argv) > 2:
    qgis_user_profile_dir = os.path.realpath(sys.argv[2])
else:
    if sys.platform.startswith('win32'):
        qgis_user_profile_dir = os.path.join(
            os.environ.get('APPDATA'),
            'QGIS/QGIS3/profiles/default'
        )
        if not os.path.isdir(qgis_user_profile_dir):
            qgis_user_profile_dir = os.path.join(
                os.environ.get('LOCALAPPDATA'),
                'QGIS/QGIS3/profiles/default'
            )
    elif sys.platform.startswith('darwin'):
        qgis_user_profile_dir = os.path.join(
            '/Users', os.environ.get('USER'),
            'Library/Application Support/QGIS/QGIS3/profiles/default'
        )


processing_log = os.path.join(qgis_user_profile_dir, 'processing/processing.log')

if not os.path.isfile(processing_log):
    print("Could not find processing log at ", processing_log)
    print("Please specify your QGIS Active Profile Folder as the second argument to this script.")
    print("(In QGIS go to 'Settings' > 'User Profiles' > 'Open Active Profile Folder' and copy the path.)")
    sys.exit(2)

with open(processing_log) as f:
    lines = f.readlines()

data_dir_regex = re.compile(r"'([^']*){0}([^']*)'".format(data_dir))
data_dir_replace_pattern = r"'\1{0}\2'.format(data_dir)"

output_file = 'qgis_commands.py'
with open(output_file, 'w') as output:
    output.write(f"""
from qgis import processing

def run(data_dir='{data_dir}'):
""")
    added_line = False
    for line in lines:
        if '|' in line:
            # line example:
            # ALGORITHM|~|2021-08-19 15:01:44|~|processing.run("native:hillshade", {'INPUT':'/Users/ksvf48/Documents/dev/pyqgis_in_a_day/srtm.tif','Z_FACTOR':1,'AZIMUTH':300,'V_ANGLE':40,'OUTPUT':'TEMPORARY_OUTPUT'})
            parts = line.strip().split('|', maxsplit=4)
            cmd = parts[4]
            if data_dir_regex.search(cmd):
                date = parts[2]
                cmd2 = data_dir_regex.sub(data_dir_replace_pattern, cmd)
                output.write(f'    # {date}\n')
                output.write(f'    {cmd2}\n')
                added_line = True

if not added_line:
    print(f"No lines matched {data_dir}.")
    sys.exit(3)

print(f"Written commands to {output_file}")
