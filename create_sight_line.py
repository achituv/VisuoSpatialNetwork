# Prepare the environment


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
from plugins.processing.algs.qgis.DeleteDuplicateGeometries import *


class SightLine:
    """This class handles all the logic about the  sight lines."""

    def __init__(self, network=None, constrains=None, res_folder=None, project=None, use='plugin'):
        """ Constrictor
         :param network to find intersections
         :param constrains the optional sight lines
         :param res_folder storing the results
         :param project loading the layers into
         :param use to identify who call that class -  plugin or standalone """

        # general attributes
        self.use = use
        # Initiate QgsApplication in case of standalone app
        if self.use == "standalone":
            self.app = QGuiApplication([])
            QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.0\apps\qgis', True)
            QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
            QgsApplication.initQgis()
        # These attributes are input from the user
        self.network = self.upload_new_layer(network, "_network")
        self.constrain = self.upload_new_layer(constrains, "_constrain")
        self.feedback = QgsProcessingFeedback()
        self.res_folder = res_folder

        # These will be used latter
        self.res = []

        # layers[0] = intersections
        # layers[1] =  edges
        self.layers = []

        # attributes to create QgsVectorLayer in memory
        self.vl = QgsVectorLayer()
        # QgsVectorDataProvider
        self.lines = None
        # QgsProject.instance()
        self.project = project

    def intersections_points(self):
        """Upload input data"""
        try:
            junc_loc_0 = os.path.dirname(__file__) + r'/processing/intersections_0.shp'

            # Find intersections points
            params = {'INPUT': self.network, 'INTERSECT': self.network, 'INPUT_FIELDS': [], 'INTERSECT_FIELDS': [],
                      'OUTPUT': junc_loc_0}

            self.res = processing.run('native:lineintersections', params, feedback=self.feedback)
            print("intersections_points is success")
        except:
            print("intersections_points is failed")

    def reproject(self, layers_to_project_path):
        """Reproject all input layers to 3857 CRS"""
        try:
            for layer in layers_to_project_path:
                # the name for the new reproject file
                my_array = layer.split('/')
                name = my_array[len(my_array) - 1].split('.')[0]
                output = os.path.dirname(__file__) + r'/processing/' + name + '_re.shp'
                params = {'INPUT': layer, 'TARGET_CRS': 'EPSG:3857', 'OUTPUT': output}
                processing.run("native:reprojectlayer", params, feedback=self.feedback)
            print("reproject is success")
            return 0
        except:
            print("reproject is failed")
            return 1

    def delete_duplicate_geometries(self):
        """Delete duplicate geometries in intesections_0 layer"""
        try:
            junc_loc = os.path.dirname(__file__) + r'/processing/intersections.shp'
            alg = DeleteDuplicateGeometries()
            alg.initAlgorithm()
            context = QgsProcessingContext()
            intersections_0 = self.upload_new_layer(self.res['OUTPUT'], "_intersections_0")
            params = {'INPUT': intersections_0, 'OUTPUT': junc_loc}
            self.res = alg.processAlgorithm(params, context, feedback=self.feedback)
            print("delete_duplicate_geometries is success")
        except:
            print("delete_duplicate_geometries is failed")

    def create_sight_lines_pot(self):
        """create lines based on the intersections"""
        try:

            # Upload intersection layers
            final = r"C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax\test\POI\results_file\final.shp"
            self.layers.append(self.upload_new_layer(final, "all_pnts"))
            # Save points with python dataset
            junctions_features = self.layers[0].getFeatures()
            python_geo = list()
            for feature in junctions_features:
                python_geo.append(feature.geometry())

            # Populate line file with potential sight of lines
            layer_path = os.path.dirname(__file__) + r'/processing/new_lines.shp'
            layer = self.upload_new_layer(layer_path, "layer")
            layer.dataProvider().truncate()

            fields = QgsFields()
            fields.append(QgsField("from", QVariant.Int))
            fields.append(QgsField("to", QVariant.Int))
            featureList = []
            for i, feature in enumerate(python_geo):
                for j in range(i + 1, len(python_geo)):
                    # Add geometry to lines' features  - the nodes of each line
                    feat = QgsFeature()
                    gLine = QgsGeometry.fromPolylineXY([feature.asPoint(), python_geo[j].asPoint()])
                    feat.setGeometry(gLine)
                    # Add  the nodes id as attributes to lines' features
                    feat.setFields(fields)
                    feat.setAttributes([i, j])
                    featureList.append(feat)
            layer.dataProvider().addFeatures(featureList)

            return True
        except:
            return False

    def find_sight_line(self):
        """Run native algorithm ( in C++) to find sight line)"""
        try:
            intersect = os.path.dirname(__file__) + r'/processing/buildings_0_re.shp'
            line_path = os.path.dirname(__file__) + r'/processing/new_lines.shp'
            params = {'INPUT': line_path, 'PREDICATE': [2], 'INTERSECT': intersect,
                      'OUTPUT': self.res_folder + '/sight_line.shp'}
            self.res = processing.run('native:extractbylocation', params, feedback=self.feedback)
            self.layers.append(self.upload_new_layer(self.res['OUTPUT'], "_sight_line"))
            return True
        except:
            return False

    def create_gdf_file(self):
        """create gdf file"""
        try:
            # Open text file as gdf file
            file1 = open(self.res_folder + '/GDFFile.gdf', "w")
            # Write intersection nodes to file
            title = "nodedef>name VARCHAR,x DOUBLE,y DOUBLE,size DOUBLE"
            file1.write(title)
            nodes_features = self.layers[0].getFeatures()
            for i, feature in enumerate(nodes_features):
                file1.write('\n')
                file1.write('"' + str(i) + '"' + ',' + '"' +
                            str(feature.geometry().asPoint()[0]) + '"' + ',' + '"' + str(
                    feature.geometry().asPoint()[1]) + '"' +
                            ',' + '"10"')
            # Write sight edges to file

            # Add new field to layer
            if self.layers[1].fields()[len(self.layers[1].fields()) - 1].name() != "weight":
                self.layers[1].dataProvider().addAttributes([QgsField("weight", QVariant.Double)])
                self.layers[1].updateFields()

            # Populate weight date
            n = len(self.layers[1].fields())

            for i, f in enumerate(self.layers[1].getFeatures()):
                geom = f.geometry()
                self.layers[1].dataProvider().changeAttributeValues({i: {n - 1: 1 / geom.length() * 100}})

            file1.write('\n')
            title = "edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE"
            file1.write(title)
            edges_features = self.layers[1].getFeatures()
            for i, feature in enumerate(edges_features):
                file1.write('\n')
                file1.write(str(feature['from']) + ',' + str(feature['to']) + ',' + str(feature['weight']))
            file1.close()
            return True
        except:
            return False

    def create_new_layer(self, selected_crs, vector_type):
        """Create new shp layers"""
        # create layer
        # data = vector_type + '?crs=' + selected_crs + '&field=from:integer&field=to:integer'
        # name = r"C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax\processing\lines.shp"
        # self.vl = QgsVectorLayer(data, baseName='lines', providerLib=" ESRI Shapefile")
        # self.lines = self.vl.dataProvider()

        # Define coordinate system
        target_crs = QgsCoordinateReferenceSystem()
        target_crs.createFromOgcWmsCrs(selected_crs)
        fields = QgsFields()
        fields.append(QgsField("from", QVariant.Int))
        fields.append(QgsField("to", QVariant.Int))
        writer = QgsVectorFileWriter("new_lines5", "system", fields, vector_type, target_crs)
        if writer.hasError() != QgsVectorFileWriter.NoError:
            print("Error when creating shapefile: ", writer.errorMessage())

        # delete the writer to flush features to disk
        del writer
        path = os.path.dirname(__file__) + r'/new_lines4.shp'

        return self.upload_new_layer(path, "pot_lines")

    def upload_new_layer(self, path, name):
        """Upload shp layers"""
        layer_name = "layer" + name
        provider_name = "ogr"
        layer = QgsVectorLayer(
            path,
            layer_name,
            provider_name)
        if not layer:
            print("Layer failed to load!-" + path)
        return layer

    def add_layers_to_pro(self, layer_array):
        """Adding layers to project"""
        self.project.addMapLayers(layer_array)

    def close(self):
        """For standalone application"""
        # Exit applications
        QgsApplication.exitQgis()
        self.app.exit()
