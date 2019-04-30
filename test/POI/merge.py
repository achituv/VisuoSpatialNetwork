from qgis.core import *
import os
import sys

from PyQt5.QtGui import *
from qgis.analysis import QgsNativeAlgorithms
from qgis.PyQt.QtCore import QVariant

# Tell Python where you will get processing from
sys.path.append(r'C:\Program Files\QGIS 3.0\apps\qgis\python\plugins')
# Reference the algorithm you want to run
from plugins import processing


def upload_new_layer(path, name):
    """Upload shp layers"""
    layer_name = "layer" + name
    provider_name = "ogr"
    layer = QgsVectorLayer(
        path,
        layer_name,
        provider_name)
    return layer


if __name__ == "__main__":
    app = QGuiApplication([])
    QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.0\apps\qgis', True)
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    QgsApplication.initQgis()
    feedback = QgsProcessingFeedback()

    """Upload input data"""
    layer_2 = upload_new_layer(
        r'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax'
        r'/test\mean_close_point\mean_close_coor.shp','test1')
    layer_1 = upload_new_layer(
        r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
             r'\test\POI\results_file/extracted.shp','test2')
    layer_3 = upload_new_layer(
        r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
             r'\test\POI\results_file\off_pnts.shp','test3')
    layers = [layer_1, layer_2,layer_3]

    OUTPUT = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
             r'\test\POI\results_file\merge.shp'
    params = {'LAYERS': layers,'CRS': 'EPSG:3857', 'OUTPUT': OUTPUT}

    processing.run('native:mergevectorlayers', params, feedback=feedback)

    """For standalone application"""
    # Exit applications
    QgsApplication.exitQgis()
    app.exit()
