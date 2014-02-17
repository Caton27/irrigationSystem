from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from CreateInitialLayout import *
from CreateFlowerbedsLayout import *
from CreateMoistureSensorsLayout import *
from CreateSunlightReadingsLayout import *
from CreateRainfallReadingsLayout import *
from CreateVolumetricsLayout import *
from CreatePlantsLayout import *
from CreateRelationshipsLayout import *
from CreateHardwareLayout import *
from CreateQueriesLayout import *
from CreateAboutLayout import *
from CreateHelpLayout import *

try:
    import serial
    try:
        ser = serial.Serial("COM3", 9600, timeout = 1)
        from GetReadings import *
        simulationMode = 0
    except:
        from GetReadingsTemp import *
        simulationMode = 1
except ImportError:
    from GetReadingsTemp import *
    simulationMode = 1

import sys

class MainWindow(QMainWindow):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irrigation system")
        self.stackedLayout = QStackedLayout()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.scroll_area = QScrollArea()

        self.setMenuBar = self.menu_bar()
        self.create_windows()
        self.add_scroll_areas()
        self.add_windows()
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stackedLayout)
        self.setCentralWidget(self.central_widget)

        
    def menu_bar(self):
        self.statusBar()
        self.menubar = self.menuBar()
        
        #view menu
        #creating the flowerbeds action
        self.flowerbedsAction = QAction(QIcon(), "Flowerbeds", self)
        self.flowerbedsAction.setStatusTip("View existing flowerbeds")
        self.flowerbedsAction.triggered.connect(self.flowerbeds_view)

        #creating the moisture sensors action
        self.moistureSensorsAction = QAction(QIcon(), "Moisture Sensors", self)
        self.moistureSensorsAction.setStatusTip("View existing moisture sensors")
        self.moistureSensorsAction.triggered.connect(self.moisture_sensors_view)

        #creating the sunlight readings action
        self.sunlightReadingsAction = QAction(QIcon(), "Sunlight Readings", self)
        self.sunlightReadingsAction.setStatusTip("View past sunlight readings")
        self.sunlightReadingsAction.triggered.connect(self.sunlight_view)

        #creating the rainfall readings action
        self.rainfallReadingsAction = QAction(QIcon(), "Rainfall Readings", self)
        self.rainfallReadingsAction.setStatusTip("View past rainfall readings")
        self.rainfallReadingsAction.triggered.connect(self.rainfall_view)

        #creating the volumetrics action
        self.volumetricsAction = QAction(QIcon(), "Volumetrics", self)
        self.volumetricsAction.setStatusTip("View system volumetrics")
        self.volumetricsAction.triggered.connect(self.volumetrics_view)

        #adding actions to the view menu
        self.viewMenu = self.menubar.addMenu("View")
        self.viewMenu.addAction(self.flowerbedsAction)
        self.viewMenu.addAction(self.moistureSensorsAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.sunlightReadingsAction)
        self.viewMenu.addAction(self.rainfallReadingsAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.volumetricsAction)


        #edit menu
        #creating the plants action
        self.plantsAction = QAction(QIcon(), "Plants", self)
        self.plantsAction.setStatusTip("Edit plants")
        self.plantsAction.triggered.connect(self.plants_view)

        #creating the relationships action
        self.relationshipsAction = QAction(QIcon(), "Relationships", self)
        self.relationshipsAction.setStatusTip("Edit existing relationships")
        self.relationshipsAction.triggered.connect(self.relationships_view)

        #creating the new hardware action
        self.newHardwareAction = QAction(QIcon(), "New Hardware", self)
        self.newHardwareAction.setStatusTip("Add new hardware to the system")
        self.newHardwareAction.triggered.connect(self.hardware_view)

        #adding actions to the edit menu
        self.editMenu = self.menubar.addMenu("Edit")
        self.editMenu.addAction(self.plantsAction)
        self.editMenu.addAction(self.relationshipsAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.newHardwareAction)


        #options menu
        #creating the queries action
        self.queriesAction = QAction(QIcon(), "Queries", self)
        self.queriesAction.setStatusTip("Input custom queries")
        self.queriesAction.triggered.connect(self.queries_view)

        #adding actions to the options menu
        self.optionsMenu = self.menubar.addMenu("Options")
        self.optionsMenu.addAction(self.queriesAction)


        #help menu
        #creating the about {program name} action
        self.aboutAction = QAction(QIcon(), "About", self)
        self.aboutAction.setStatusTip("About the program")
        self.aboutAction.triggered.connect(self.about_view)

        #creating the help action
        self.helpAction = QAction(QIcon(), "Help", self)
        self.helpAction.setStatusTip("Help")
        self.helpAction.triggered.connect(self.help_view)

        #adding actions to the options menu
        self.helpMenu = self.menubar.addMenu("Help")
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.helpAction)


        #take readings
        #creating the take reading (moisture sensor) action
        self.moistureAction = QAction(QIcon(), "Take a moisture sensor reading", self)
        self.moistureAction.setStatusTip("Moisture")
        self.moistureAction.triggered.connect(self.moisture_reading_view)
        
        #creating the take reading (sunlight sensor) action
        self.sunlightAction = QAction(QIcon(), "Take a sunlight reading", self)
        self.sunlightAction.setStatusTip("Sunlight")
        self.sunlightAction.triggered.connect(self.sunlight_reading_view)
        
        #creating the take reading (rainfall sensor) action
        self.rainfallAction = QAction(QIcon(), "Take a rainfall reading", self)
        self.rainfallAction.setStatusTip("Rainfall")
        self.rainfallAction.triggered.connect(self.rainfall_reading_view)

        #adding action to the take readings menu
        self.readingsMenu = self.menubar.addMenu("Take reading")
        self.readingsMenu.addAction(self.moistureAction)
        self.readingsMenu.addAction(self.sunlightAction)
        self.readingsMenu.addAction(self.rainfallAction)


    def temp():
        pass

    def create_windows(self):
        self.initial_layout_widget = InitialLayoutWindow()
        self.flowerbeds_layout_widget = FlowerbedsWindow(self)
        self.moisture_sensors_layout_widget = MoistureSensorsWindow()
        self.sunlight_layout_widget = SunlightWindow()
        self.rainfall_layout_widget = RainfallWindow()
        self.volumetrics_layout_widget = VolumetricsWindow()
        self.plants_layout_widget = PlantsWindow()
        self.hardware_layout_widget = HardwareWindow(self)
        self.queries_layout_widget = QueryWindow()
        self.about_layout_widget = AboutWindow()
        self.help_layout_widget = HelpWindow()
        

    def add_scroll_areas(self):
        self.flowerbeds_layout_widget_with_scroll_area = QScrollArea()
        self.flowerbeds_layout_widget_with_scroll_area.setWidget(self.flowerbeds_layout_widget)

        self.moisture_sensors_layout_widget_with_scroll_area = QScrollArea()
        self.moisture_sensors_layout_widget_with_scroll_area.setWidget(self.moisture_sensors_layout_widget)

        self.plants_layout_widget_with_scroll_area = QScrollArea()
        self.plants_layout_widget_with_scroll_area.setWidget(self.plants_layout_widget)

        self.help_layout_widget_with_scroll_area = QScrollArea()
        self.help_layout_widget_with_scroll_area.setWidget(self.help_layout_widget)
        

    def add_windows(self):
        self.relationships_layout_widget_with_scroll_area = QLabel()
        self.stackedLayout.addWidget(self.initial_layout_widget)
        self.stackedLayout.addWidget(self.flowerbeds_layout_widget_with_scroll_area) #scroll area
        self.stackedLayout.addWidget(self.moisture_sensors_layout_widget_with_scroll_area)#scroll area
        self.stackedLayout.addWidget(self.sunlight_layout_widget)
        self.stackedLayout.addWidget(self.rainfall_layout_widget)
        self.stackedLayout.addWidget(self.volumetrics_layout_widget)
        self.stackedLayout.addWidget(self.plants_layout_widget_with_scroll_area)#scroll area
        self.stackedLayout.addWidget(self.relationships_layout_widget_with_scroll_area)#scroll area
        self.stackedLayout.addWidget(self.hardware_layout_widget)
        self.stackedLayout.addWidget(self.queries_layout_widget)
        self.stackedLayout.addWidget(self.about_layout_widget)
        self.stackedLayout.addWidget(self.help_layout_widget_with_scroll_area)#scroll area


    def refresh_combo_boxes_flowerbed(self):
        self.hardware_layout_widget.populate_combo_boxes()
        self.plants_layout_widget.populate_combo_boxes()

    def refresh_combo_boxes_sensor(self):
        self.moisture_sensors_layout_widget.populate_combo_boxes()

    def refresh_readings_tables_flowerbed(self):
        self.flowerbeds_layout_widget.select_flowerbed()
        self.moisture_sensors_layout_widget.select_moisture_sensors()

    def refresh_readings_tables(self):
        self.rainfall_layout_widget.select_timeframe()
        self.sunlight_layout_widget.select_timeframe()

    def refresh_values(self):
        self.volumetrics_layout_widget.update_values()


    def flowerbeds_view(self):
        self.stackedLayout.setCurrentIndex(1)
        self.setWindowTitle("Irrigation system - View Flowerbeds")
        window.resize(800,550)

    def moisture_sensors_view(self):
        self.stackedLayout.setCurrentIndex(2)
        self.setWindowTitle("Irrigation system - View Moisture Sensors")
        window.resize(500,450)

    def sunlight_view(self):
        self.stackedLayout.setCurrentIndex(3)
        self.setWindowTitle("Irrigation system - View Sunlight Readings")
        window.resize(600,400)

    def rainfall_view(self):
        self.stackedLayout.setCurrentIndex(4)
        self.setWindowTitle("Irrigation system - View Rainfall Readings")
        window.resize(500,400)

    def volumetrics_view(self):
        self.stackedLayout.setCurrentIndex(5)
        self.setWindowTitle("Irrigation system - View Volumetrics")
        window.resize(500,400)

    def plants_view(self):
        self.stackedLayout.setCurrentIndex(6)
        self.setWindowTitle("Irrigation system - Edit Plants")
        window.resize(650,450)

    def relationships_view(self):
        self.stackedLayout.removeWidget(self.relationships_layout_widget_with_scroll_area)
        self.relationships_layout_widget_with_scroll_area = QScrollArea()
        self.relationships_layout_widget_with_scroll_area.setWidget(RelationshipsWindow())
        self.stackedLayout.insertWidget(7, self.relationships_layout_widget_with_scroll_area)
        self.stackedLayout.setCurrentIndex(7)
        self.setWindowTitle("Irrigation system - Edit Relationships")
        window.resize(500,600)

    def hardware_view(self):
        self.stackedLayout.setCurrentIndex(8)
        self.setWindowTitle("Irrigation system - Add hardware")
        window.resize(400,400)

    def queries_view(self):
        self.stackedLayout.setCurrentIndex(9)
        self.setWindowTitle("Irrigation system - Custom queries")
        window.resize(600,500)

    def about_view(self):
        self.stackedLayout.setCurrentIndex(10)
        self.setWindowTitle("Irrigation system - About")
        window.resize(400,400)

    def help_view(self):
        self.stackedLayout.setCurrentIndex(11)
        self.setWindowTitle("Irrigation system - Help")
        window.resize(400,450)

    def moisture_reading_view(self):
        newReadings = get_new_readings_moisture()
        add_to_database_moisture(newReadings)
        operations = calculate_need(newReadings)
        if simulationMode == 0:
            water_plants(operations)
        confirm_message = QMessageBox()
        confirm_message.setText("Moisture sensor reading(s) taken and stored")
        confirm_message.exec_()
        self.refresh_readings_tables_flowerbed()
        self.refresh_values()

    def sunlight_reading_view(self):
        newReadings = get_new_readings_sunlight()
        add_to_database_sunlight(newReadings)
        confirm_message = QMessageBox()
        confirm_message.setText("Sunlight reading taken and stored")
        confirm_message.exec_()
        self.refresh_readings_tables()

    def rainfall_reading_view(self):
        newReadings = get_new_readings_rainfall()
        add_to_database_rainfall(newReadings)
        confirm_message = QMessageBox()
        confirm_message.setText("Rainfall reading taken and stored")
        confirm_message.exec_()
        self.refresh_readings_tables()
    
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    window.resize(600,450)
    application.exec_()
    
