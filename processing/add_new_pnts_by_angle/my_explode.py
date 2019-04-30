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
from plugins.processing.algs.qgis.Explode import *


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

    input = os.path.dirname(os.path.dirname(__file__)) + r'/dissolve_0.shp'

    OUTPUT = os.path.dirname(__file__) + r'/explode.shp'

    alg = Explode()
    alg.initAlgorithm()
    context = QgsProcessingContext()
    params = {'INPUT': input, 'OUTPUT': OUTPUT}
    res = alg.processAlgorithm(params, context, feedback=feedback)

    """For standalone application"""
    # Exit applications
    QgsApplication.exitQgis()
    app.exit()
