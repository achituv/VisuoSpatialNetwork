
# from test.mean_close_point.mean_close_point import *
# from test.POI.main import *
import time


def run_logic(method):
    time_1 = time.time()
    if method():
        print(method.__name__, str(time.time() - time_1))
    else:
        print("Error", method.__name__ + " does't work")



if __name__ == "__main__":
    import sys
    sys.path.append(r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax')

    from QGIS import *
    from create_sight_line import *

    # print(os.environ['PATH'])
    # my_sight_line = SightLine("test")
    network_temp = os.path.dirname(__file__) + r'/processing/highways_0.shp'
    constrains_temp = os.path.dirname(__file__) + r'/processing/buildings_0.shp'
    poi_temp = os.path.dirname(__file__) + r'/processing/poi.shp'
    res_folder = os.path.dirname(__file__) + r'/results'
    my_sight_line = SightLine(network_temp, constrains_temp, res_folder, NULL, "standalone")


    # Reproject layers files
    my_sight_line.reproject([network_temp, constrains_temp, poi_temp])

    # Define intersections only between more than 2 lines
    network_re = os.path.dirname(__file__) + r'/processing/highways_0_re.shp'
    myQGIS("standalone", network_re, "_lines")
    #
    # # poi = os.path.dirname(__file__) + r'/processing/poi_re.shp'
    #
    # # Find intersections
    # network_new = os.path.dirname(__file__) + r'/processing/dissolve_0.shp'
    # my_sight_line.network = my_sight_line.upload_new_layer(network_new,"network_new")
    # my_sight_line.intersections_points()
    # my_sight_line.delete_duplicate_geometries()
    #
    # # Calculate mean for close points
    # MeanClosePoint('standalone')
    #
    # # Projection for POI inside polygons and all POI to  intersections
    # add_poi_to_intersections('standalone')
    #
    # # Calc sight lines
    # network_dissolve = os.path.dirname(__file__) + r'/processing/dissolve_0.shp'
    # buildings_0_re = os.path.dirname(__file__) + r'/processing/buildings_0_re.shp'
    # my_sight_line.network = my_sight_line.upload_new_layer(network_dissolve,"dissolve")
    # my_sight_line.constrain = my_sight_line.upload_new_layer(buildings_0_re,"projected")
    #
    # run_logic(my_sight_line.create_sight_lines_pot)
    # run_logic(my_sight_line.find_sight_line)
    # run_logic(my_sight_line.create_gdf_file)
