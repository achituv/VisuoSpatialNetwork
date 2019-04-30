from qgis.core import *

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtCore import *




# Add new features
def add_new_feature(layer, feature):
    feat = QgsFeature(layer.fields())
    feat.setGeometry(feature.geometry())
    layer.dataProvider().addFeatures([feat])


# Create gdf file with nodes and edges shape files
def create_gdf_file(nodes, edges):
    # Open text file as gdf file
    file1 = open("GDFFile.gdf", "w")
    # Write intersection nodes to file
    title = "nodedef>name VARCHAR,x DOUBLE,y DOUBLE ,size DOUBLE"
    file1.write(title)
    nodes_features = nodes.getFeatures()
    for i, feature in enumerate(nodes_features):
        file1.write('\n')
        file1.write(str(i) + ',' + str(feature.geometry().asPoint()[0]) + ',' + str(feature.geometry().asPoint()[1]) +
                    '5')
    # Write sight edges to file
    file1.write('\n')
    title = "edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE"
    file1.write(title)
    edges_features = edges.getFeatures()
    for i, feature in enumerate(edges_features):
        file1.write('\n')
        file1.write(str(i) + ',' + str(feature['from']) + ',' + str(feature['to']))
    file1.close()
