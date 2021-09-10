
from qgis import processing

def run(data_dir):
    # 2021-08-12 16:20:38
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}/110m_physical/ne_110m_rivers_lake_centerlines.shp|layerid=0|subset=\"min_zoom\" <= 0'.format(data_dir),'CALC_METHOD':2,'OUTPUT':'TEMPORARY_OUTPUT'})
    # 2021-08-12 16:23:55
    processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'{0}/10m_cultural/ne_10m_roads.shp|layerid=0|subset=\"min_zoom\" <= 5'.format(data_dir),'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})
