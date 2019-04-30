from qgis.core import *
import os
import sys

from PyQt5.QtGui import *
from qgis.analysis import QgsNativeAlgorithms

# Tell Python where you will get processing from
sys.path.append(r'C:\Program Files\QGIS 3.0\apps\qgis\python\plugins')
# Reference the algorithm you want to run
from plugins import processing
from plugins.processing.algs.qgis.DeleteDuplicateGeometries import *


def upload_new_layer(self, path, name):
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
    # processing.run("native:dissolve",
    #                {'INPUT':'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax/'
    #                         'processing/highways_1.shp','FIELD':['group'],'OUTPUT':'memory:'},feedback )

    """Upload input data"""

    junc_loc_0 = os.path.dirname(__file__) + r'/processing/dissolve_0.shp'
    network = os.path.dirname(__file__) + r'/processing/highways_1.shp'
    # network = QgsVectorLayer(
    #     network,
    #     "test",
    #     "ogr")
    # Find intersections points
    params = {'INPUT': network, 'FIELD': 'group', 'OUTPUT': junc_loc_0}

    processing.run('native:dissolve', params, feedback=feedback)

    """For standalone application"""
    # Exit applications
    QgsApplication.exitQgis()
    app.exit()


