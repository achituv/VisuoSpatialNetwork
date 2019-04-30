# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VisibilitySyntax
                                 A QGIS plugin
 The plugin calculate visibility metrics
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-09-20
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Achituv Cohen
        email                : achic19@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtGui import *
from qgis.PyQt.QtCore import *
from PyQt5.QtWidgets import QAction, QFileDialog
import sys

sys.path.append(r'C:\Users\achituv\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\visibilitysyntax')
import time

from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .visibility_syntax_dialog import VisibilitySyntaxDialog
from .test.mean_close_point.mean_close_point import *
from .test.POI.main import *
import os.path

# Import my code
# Tell Python where you will get processing from
# from .create_sight_line3 import *
from create_sight_line import *
from QGIS import *


class VisibilitySyntax:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'VisibilitySyntax_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = VisibilitySyntaxDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Visibility Syntax')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'VisibilitySyntax')
        self.toolbar.setObjectName(u'VisibilitySyntax')

        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_folder)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VisibilitySyntax', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/visibility_syntax/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u' Calculate visibility metrics'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Visibility Syntax'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # Upload directory location to store results
    def select_output_folder(self):

        self.filename = QFileDialog.getExistingDirectory(self.dlg, "Select output folder ", "")
        self.dlg.lineEdit.setText(str(self.filename))

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Get all loaded layers in the interface
        layers = self.iface.mapCanvas().layers()
        # Get all loaded layers in the interface
        layer_list = []
        for layer in layers:
            # Add it to the list
            layer_list.append(layer.name())
        # Clear comboBox (useful so we don't create duplicate items in list)
        self.dlg.comboBox.clear()
        # Add all items in list to comboBox
        self.dlg.comboBox.addItems(layer_list)
        # Clear comboBox_2
        self.dlg.comboBox_2.clear()
        # Add all items in list to comboBox_2
        self.dlg.comboBox_2.addItems(layer_list)
        # Clear comboBox_3
        self.dlg.comboBox_3.clear()
        # Add all items in list to comboBox_3
        self.dlg.comboBox_3.addItems(layer_list)

        # Identify network layer by its index and get his path
        selectedLayerIndex = self.dlg.comboBox.currentIndex()
        network = layers[selectedLayerIndex]
        network_temp = network.dataProvider().dataSourceUri()
        network_path = str.split(network_temp, '|')[0]

        # Identify constrains layer by its index and get his path
        selectedLayerIndex_2 = self.dlg.comboBox_2.currentIndex()
        constrains = layers[selectedLayerIndex_2]
        constrains_temp = constrains.dataProvider().dataSourceUri()
        constrains_path = str.split(constrains_temp, '|')[0]

        # Identify Point Of Interest layer by its index and get his path
        selectedLayerIndex_3 = self.dlg.comboBox_3.currentIndex()
        poi = layers[selectedLayerIndex_3]
        poi_temp = poi.dataProvider().dataSourceUri()
        poi_path = str.split(poi_temp, '|')[0]

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # The logic behind the plugin
            # Test
            network_path = os.path.dirname(__file__) + r'/processing/highways_0.shp'
            constrains_path = os.path.dirname(__file__) + r'/processing/buildings_0.shp'
            poi_path = os.path.dirname(__file__) + r'/processing/poi.shp'
            self.filename = os.path.dirname(__file__) + r'/results'
            self.iface.messageBar().pushMessage(str(self.dlg.checkBox.checkState()), level=Qgis.Info)


            # # # Build sight line object
            # my_sight_line = SightLine(network_path, constrains_path, self.filename
            #                           , QgsProject.instance())
            # # Reproject layers files
            # my_sight_line.reproject([network_path, constrains_path, poi_path])
            #
            # # Define intersections only between more than 2 lines
            # network_re = os.path.dirname(__file__) + r'/processing/highways_0_re.shp'
            # myQGIS("plugin", network_re, "_lines")
            #
            # # Find intersections
            # network_new = os.path.dirname(__file__) + r'/processing/dissolve_0.shp'
            # my_sight_line.network = my_sight_line.upload_new_layer(network_new, "network_new")
            # my_sight_line.intersections_points()
            # my_sight_line.delete_duplicate_geometries()
            #
            # # # Calculate mean for close points
            # MeanClosePoint()
            #
            # # Projection for POI inside polygons and all POI to  intersections
            # add_poi_to_intersections()
            #
            # # Calc sight lines
            # network_dissolve = os.path.dirname(__file__) + r'/processing/dissolve_0.shp'
            # buildings_0_re = os.path.dirname(__file__) + r'/processing/buildings_0_re.shp'
            # my_sight_line.network = my_sight_line.upload_new_layer(network_dissolve, "dissolve")
            # my_sight_line.constrain = my_sight_line.upload_new_layer(buildings_0_re, "projected")
            #
            #
            # my_sight_line.create_sight_lines_pot()
            # my_sight_line.find_sight_line()
            # my_sight_line.create_gdf_file()

    def run_logic(self, method):
        # Message to user for each step
        time_1 = time.time()
        if method():
            self.iface.messageBar().pushMessage(method.__name__, str(time.time() - time_1) + "_8", level=Qgis.Info)
        else:
            self.iface.messageBar().pushMessage("Error", method.__name__ + " does't work", level=Qgis.Critical)