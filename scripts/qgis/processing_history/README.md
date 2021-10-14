# Turn processing history into an executable python script

`convert_history_to_python.py` looks in your QGIS processing log for processing commands run in a given data directory,
and exports them as an executable file. This file can then be pushed to github or included in a data deposit, to enable
others to reproduce your analysis.

N.B. This script is still a work in progress - see the [GitHub issues](https://github.com/alisonrclarke/domain-specific-software-sustainability/issues) for a list of fixes to be made.

## Exporting history

To export QGIS processing history based on a given data directory (do **either** 1 **or** 2):

1.  **From the command line, if you have python installed**:

    Change directory to the location of `convert_history_to_python`, (e.g. `/Users/ksvf48/Documents/GitHub/domain-specific-software-sustainability/scripts/qgis/processing_history`) and run:

    ```bash
    python convert_history_to_python.py <data_dir>
    ```

    e.g. if data is stored in `/Users/ksvf48/Documents/dev/pyqgis_in_a_day`

    ```bash
    python convert_history_to_python.py /Users/ksvf48/Documents/dev/pyqgis_in_a_day
    ```

2.  **From QGIS**:

    1. Open the python console.
    2. Type the following, replacing `<location>` with the location where this directory is checked out, e.g. `sys.path.append('/Users/ksvf48/Documents/GitHub/domain-specific-software-sustainability/scripts/qgis/processing_history')`, and `<data_dir>` with the directory where your input data is stored:

      ```python
      sys.path.append('<location>')
      import convert_history_to_python
      convert_history_to_python.convert_history_to_python('<data_dir>')
      ```

`convert_history_to_python` exports a file `qgis_commands.py` in a timestamped folder within an `outputs` directory of this directory (e.g. `outputs/2021-10-04_155206/qgis_commands.py`), which contains all the QGIS processing done on files within the given data directory.

Example `qgis_commands.py` file:

```python
from qgis import processing
from qgis.core import QgsMessageLog

def run(data_dir='/Users/ksvf48/Downloads/packages/Natural_Earth_quick_start/'):
    # 2021-08-12 16:20:38
    QgsMessageLog.logMessage("Running command: processing.run(\"qgis:exportaddgeometrycolumns\", {'INPUT':'{0}110m_physical/ne_110m_rivers_lake_centerlines.shp|layerid=0|subset=\"min_zoom\" <= 0'.format(data_dir),'CALC_METHOD':2,'OUTPUT':'TEMPORARY_OUTPUT'})")
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}110m_physical/ne_110m_rivers_lake_centerlines.shp|layerid=0|subset=\"min_zoom\" <= 0'.format(data_dir),'CALC_METHOD':2,'OUTPUT':'TEMPORARY_OUTPUT'})
    # 2021-08-12 16:23:55
    QgsMessageLog.logMessage("Running command: processing.run(\"qgis:exportaddgeometrycolumns\", {'INPUT':'{0}10m_cultural/ne_10m_roads.shp|layerid=0|subset=\"min_zoom\" <= 5'.format(data_dir),'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})")
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}10m_cultural/ne_10m_roads.shp|layerid=0|subset=\"min_zoom\" <= 5'.format(data_dir),'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})
```

If necessary, this file could be edited by hand to remove duplicate entries (e.g. if an analysis was retried with different parameters).

The exported file could then be stored in version control.

You can choose to output the file to a different location `<output_script_dir>` as follows:

1.  **From the command line**:

    ```bash
    python convert_history_to_python.py <data_dir> <output_script_dir>
    ```

2.  **From QGIS**:

    ```python
    convert_history_to_python.convert_history_to_python('<data_dir>', '<output_script_dir>')
    ```

(Note that the file will still be in a timestamped directory and called `qgis_processing.py`.)

## Running the exported script

To rerun the processing from QGIS:

1. Open the python console.
2. Run the following commands, replacing `<script_dir>` with the folder where `qgis_commands.py` is (e.g. `/Users/ksvf48/Documents/dev/domain-specific-software-sustainability/scripts/qgis/processing/outputs/2021-10-04_155206`):

  ```python
  sys.path.append('<script_dir>')
  import qgis_commands
  qgis_commands.run()
  ```

  If you want to run the commands on a different system with a different data path, modify the last line to the following, replacing `<data_dir>` with the folder where your data files are:

  ```python
  qgis_commands.run('<data_dir>')
  ```
