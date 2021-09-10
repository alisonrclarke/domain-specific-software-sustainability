# Turn processing history into an executable python script

To export QGIS processing history based on a given data directory:

```
python convert_history_to_python.py <data_dir>
```

e.g. if data is stored in `/Users/ksvf48/Documents/dev/pyqgis_in_a_day`

```
python convert_history_to_python.py /Users/ksvf48/Documents/dev/pyqgis_in_a_day
```

This exports a file `qgis_commands.py` in the current working directory which contains all the qGIS processing done on files within that folder.

e.g.

```
from qgis import processing

def run(data_dir):
    # 2021-08-12 16:20:38
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}/110m_physical/ne_110m_rivers_lake_centerlines.shp|layerid=0|subset=\"min_zoom\" <= 0'.format(data_dir),'CALC_METHOD':2,'OUTPUT':'TEMPORARY_OUTPUT'})
    # 2021-08-12 16:23:55
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}/10m_cultural/ne_10m_roads.shp|layerid=0|subset=\"min_zoom\" <= 5'.format(data_dir),'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})
```

If necessary, this file could be edited by hand to remove duplicate entries (e.g. if an analysis was retried with differenr parameters).

The exported file could then be stored in version control.

To rerun the processing from qGIS:

1. Open the python console.
2. Run the following commands, replacing `<script_dir>` with the folder where `qgis_commands.py` is (e.g. `/Users/ksvf48/Documents/dev/domain-specific-software-sustainability/scripts/qgis/processing`):

  ```
  import qgis_commands
  qgis_commands.run()
  ```
