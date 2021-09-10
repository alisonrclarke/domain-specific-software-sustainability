import os
import re
import sys

if len(sys.argv) < 2:
    print("No data dir specified - exiting")
    sys.exit(1)

data_dir = sys.argv[1]

# FIXME: make this work on other platforms
qgis_user_profile_dir=os.path.join('/Users', os.environ.get('USER'), 'Library/Application Support/QGIS/QGIS3/profiles/default')

processing_log=os.path.join(qgis_user_profile_dir, 'processing/processing.log')

if not os.path.isfile(processing_log):
    print("Could not find processing log at ", processing_log)
    sys.exit(2)

with open(processing_log) as f:
    lines = f.readlines()

data_dir_regex = re.compile(r"'([^']*){0}([^']*)'".format(data_dir))
data_dir_replace_pattern = r"'\1{0}\2'.format(data_dir)"

output_file = 'qgis_commands.py'
with open(output_file, 'w') as output:
    output.write("""
from qgis import processing

def run(data_dir):
""")

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
