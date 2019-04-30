from qgis.core import *
import os
import sys

from PyQt5.QtGui import *
from qgis.analysis import QgsNativeAlgorithms
from qgis.PyQt.QtCore import QVariant


# Tell Python where you will get processing from
sys.path.append(r'C:\Program Files\QGIS 3.0\apps\qgis\python\plugins')
# Reference the algorithms you want to run
from plugins import processing
from plugins.processing.algs.qgis.HubDistanceLines import *
from plugins.processing.algs.qgis.PointDistance import *
from plugins.processing.algs.qgis.PointsAlongGeometry import *
from plugins.processing.algs.qgis.PolygonsToLines import *
from plugins.processing.algs.qgis.DeleteDuplicateGeometries import *


def upload_new_layer(path, name):
    """Upload shp layers"""
    layer_name = "layer" + name
    provider_name = "ogr"
    layer = QgsVectorLayer(
        path,
        layer_name,
        provider_name)
    return layer


def add_poi_to_intersections(use='plugin'):
    if use == "standalone":
        app = QGuiApplication([])
        QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.0\apps\qgis', True)
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        QgsApplication.initQgis()
    feedback = QgsProcessingFeedback()

    """ implement Clip """
    try:
        """Upload input data"""

        input = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                r'/processing/poi_re.shp'
        overlay = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax' \
                  '/processing/buildings_0_re.shp'
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file/cliped.shp'
        params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}

        processing.run('native:clip', params, feedback=feedback)
        print("Clip success")

    except:
        print("Clip failed")

    """ implement Extract """
    try:
        """Upload input data"""

        input = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax/' \
                'processing/poi_re.shp'
        intersect = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax/' \
                    'processing/buildings_0_re.shp'
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file/extracted.shp'
        params = {'INPUT': input, 'PREDICATE': [2], 'INTERSECT': intersect, 'OUTPUT': output}

        processing.run('native:extractbylocation', params, feedback=feedback)
        print("Extract success")
    except:
        print("Extract failed")

    """ implement Point along geometry """
    try:
        input = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax' \
                '/processing/highways_0_re.shp'
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file/points_along.shp'

        alg = PointsAlongGeometry()
        alg.initAlgorithm()
        context = QgsProcessingContext()
        params = {'INPUT': input, 'DISTANCE': 10, 'START_OFFSET': 0, 'END_OFFSET': 0, 'OUTPUT': output}
        res = alg.processAlgorithm(params, context, feedback=feedback)
        print("Point along geometry success")
    except:
        print("Point along geometry failed")

    """implement add ID"""
    try:
        hub_path = os.path.dirname(__file__) + r'/results_file/points_along.shp'
        junc = upload_new_layer(hub_path, "hub")
        if junc.fields()[len(junc.fields()) - 1].name() != "vis_id":
            junc.dataProvider().addAttributes([QgsField("vis_id", QVariant.Int)])
            junc.updateFields()
        n = len(junc.fields())
        for i, feature in enumerate(junc.getFeatures()):
            junc.dataProvider().changeAttributeValues({i: {n - 1: i}})
        print("add ID success")

    except:
        print("add ID failed")

    """ implement Distance to nearest hub   """
    try:
        """Upload input data"""

        input_path = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                     r'\test\POI\results_file/cliped.shp'
        input = upload_new_layer(input_path, "test_input")
        hubs_path = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                    r'\test\POI\results_file/points_along.shp'
        hubs = upload_new_layer(hubs_path, "test_hubs_")
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file/line_to_points.shp'

        alg = HubDistanceLines()
        alg.initAlgorithm()
        # Some preprocessing for context
        project = QgsProject.instance()

        target_crs = QgsCoordinateReferenceSystem()
        target_crs.createFromOgcWmsCrs(input.crs().authid())
        project.setCrs(target_crs)
        context = QgsProcessingContext()
        context.setProject(project)
        params = {'INPUT': input, 'HUBS': hubs, 'FIELD': 'vis_id', 'UNIT': 4, 'OUTPUT': output}
        alg.processAlgorithm(params, context, feedback=feedback)
        print("Distance to nearest hub success")
    except:
        print("Distance to nearest hub  failed")

    """ implement  Polygon to lines  """
    try:
        input = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax/' \
                'processing/buildings_0_re.shp'
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file\poly_as_lines.shp'

        alg = PolygonsToLines()
        alg.initAlgorithm()
        context = QgsProcessingContext()
        params = {'INPUT': input, 'OUTPUT': output}
        res = alg.processAlgorithm(params, context, feedback=feedback)
        print(" Polygon to lines success")
    except:
        print(" Polygon to lines failed")

    """ implement Line intersections  """
    try:
        """Upload input data"""

        input_path = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                     r'\test\POI\results_file\line_to_points.shp'
        input = upload_new_layer(input_path, "test_input")
        intersect_path = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                         r'\test\POI\results_file\poly_as_lines.shp'
        intersect = upload_new_layer(intersect_path, "test_intersect")
        output = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file\off_pnts.shp'
        params = {'INPUT': input, 'INTERSECT': intersect, 'INPUT_FIELDS': [], 'INTERSECT_FIELDS': [], 'OUTPUT': output}

        processing.run('native:lineintersections', params, feedback=feedback)
        print("Line intersections success")
    except:
        print("Line intersections failed")

    """ implement Merge  """
    try:
        layer_2 = upload_new_layer(
            r'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax'
            r'/test\mean_close_point\mean_close_coor.shp', 'test1')
        layer_1 = upload_new_layer(
            r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
            r'\test\POI\results_file/extracted.shp', 'test2')
        layer_3 = upload_new_layer(
            r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
            r'\test\POI\results_file\off_pnts.shp', 'test3')
        layers = [layer_1, layer_2, layer_3]

        OUTPUT = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax' \
                 r'\test\POI\results_file\merge.shp'
        params = {'LAYERS': layers, 'CRS': 'EPSG:3857', 'OUTPUT': OUTPUT}

        processing.run('native:mergevectorlayers', params, feedback=feedback)
        print("Merge success")
    except:
        print("Merge failed")

    """ implement Delete Duplicate geometry """
    try:

        """Upload input data"""

        feedback = QgsProcessingFeedback()

        """Upload input data"""

        input = 'C:/Users/achituv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/visibilitysyntax/test/POI' \
                '/results_file/merge.shp'

        OUTPUT = r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax\test\POI' \
                 r'\results_file\final.shp'

        alg = DeleteDuplicateGeometries()
        alg.initAlgorithm()
        context = QgsProcessingContext()
        params = {'INPUT': input, 'OUTPUT': OUTPUT}
        res = alg.processAlgorithm(params, context, feedback=feedback)

        print("Delete Duplicate geometry  success")
    except:
        print("Delete Duplicate geometry  failed")

    """For standalone application"""
    if use == 'standalone':
        QgsApplication.exitQgis()
        app.exit()

if __name__ == "__main__":
    add_poi_to_intersections()


