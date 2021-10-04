# Turn processing history into an executable python script

`convert_history_to_python.py` looks in your QGIS processing log for processing commands run in a given data directory,
and exports them as an executable file. This file can then be pushed to github or included in a data deposit, to enable
others to reproduce your analysis.

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

    a. Open the python console.
    b. Type the following, replacing `<location>` with the location where this directory is checked out, e.g. `sys.path.append('/Users/ksvf48/Documents/GitHub/domain-specific-software-sustainability/scripts/qgis/processing_history')`, and `<data_dir>` with the directory where your input data is stored:

    ```python
    sys.path.append('<location>')
    import convert_history_to_python
    convert_history_to_python.convert_history_to_python('<data_dir>')
    ```

`convert_history_to_python` exports a file `qgis_commands.py` in the current working directory which contains all the qGIS processing done on files within that folder.

e.g.

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

## Running the exported script

To rerun the processing from QGIS:

1. Open the python console.
2. Run the following commands, replacing `<script_dir>` with the folder where `qgis_commands.py` is (e.g. `/Users/ksvf48/Documents/dev/domain-specific-software-sustainability/scripts/qgis/processing`):

  ```
  sys.path.append('<script_dir>')
  import qgis_commands
  qgis_commands.run()
  ```

  If you want to run the commands on a different system with a different data path, modify the last line to the following, replacing `<data_dir>` with the folder where your data files are:

  ```
  qgis_commands.run('<data_dir>')
  ```
