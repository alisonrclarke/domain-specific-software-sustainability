import os
import re
import sys


def convert_history_to_python(data_dir, qgis_user_profile_dir=None):
    if qgis_user_profile_dir is None:
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

    data_dir = data_dir.rstrip('/\\')

    # Match single-quoted strings that contain data_dir, ensuring that escaped
    # single quotes don't end the match
    data_dir_regex = re.compile(r"'(?P<input_file_start>.*?){0}(?P<input_file_end>.*?)(?<!\\)'".format(data_dir))
    data_dir_replace_pattern = r"'\g<input_file_start>{0}\g<input_file_end>'.format(data_dir)"

    # Match outputs so we can create the output directory
    output_file_regex = re.compile(r"'OUTPUT[^']*':'(.*?)(?<!\\)'")

    # FIXME: add this script directory (for now) or output_dir
    output_file = os.path.dirname(os.path.abspath(__file__)) + '/qgis_commands.py'
    with open(output_file, 'w') as output:
        output.write(f"""
import os
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
                    output.write(f'    # {date}\n')

                    output_cmd = data_dir_regex.sub(data_dir_replace_pattern, cmd)
                    output_cmd_quoted = re.sub(r'(?<!\\)"','\\"', output_cmd)
                    print(f"Adding command: {output_cmd_quoted}")
                    output.write(f'    print("Running command: {output_cmd_quoted}")\n')

                    output_matches = output_file_regex.search(cmd)
                    if output_matches:
                        current_output_file = output_matches.group(1)
                        if data_dir in current_output_file:
                            current_output_dir = os.path.dirname(current_output_file)
                            current_output_dir = current_output_dir.replace(data_dir, '{0}')
                            output.write(f'    os.makedirs("{current_output_dir}".format(data_dir), exist_ok=True)\n')

                    output.write(f'    {output_cmd}\n')
                    added_line = True

    if not added_line:
        print(f"No lines matched {data_dir}.")
        sys.exit(3)

    print(f"Written commands to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No input data dir specified - exiting")
        sys.exit(1)

    data_dir = sys.argv[1]
    qgis_user_profile_dir = None

    if len(sys.argv) > 2:
        qgis_user_profile_dir = os.path.realpath(sys.argv[2])

    convert_history_to_python(data_dir, qgis_user_profile_dir)
