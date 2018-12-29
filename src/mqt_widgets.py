import os

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import * 
from mqt_icons        import MQT_ICON
from mqt_icons        import MQT_PIXMAP
from mqt_constants    import *
from time             import gmtime
from time             import strftime

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Button(QPushButton):

    def __init__(self,icon_normal,icon_hover,tooltip):

        QPushButton.__init__(self)    

        _css  = """
            border: 0px solid gray;
            background-color: #FFFFFF;
        """ 

        self.setStyleSheet(_css)

        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover
        
        self.setToolTip(tooltip)
        self.setIcon(QIcon(self.icon_normal))

    def enterEvent(self, event):

        self.setIcon(QIcon(self.icon_hover))

    def leaveEvent(self, event):

        self.setIcon(QIcon(self.icon_normal))

    def register_button_clbk(self,clbk):

        self.clicked.connect(clbk)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Window(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.setWindowTitle("Mathematical Sets Visualisation")
        self.setWindowIcon(MQT_ICON("mqt"))
        self.setFixedSize(CST_WINDOW_WIDTH, CST_WINDOW_HEIGHT)
        self.setStyleSheet("background-color: #FFFFFF; border: 0px;")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.status = MQT_WDG_StatusBar()
        self.setStatusBar(self.status)  

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Vertical_Toolbar(QToolBar):

    def __init__(self):

        QToolBar.__init__(self)
        self.setOrientation(Qt.Horizontal)

        self.wdg_resolution = MQT_WDG_Slider("Resolution")

        self.addWidget(self.wdg_resolution)

    def register_resolution_clbk(self,clbk):

        self.wdg_resolution.register_value_changed(clbk)

    def set_resolution_boundry(self,min,max,value):

        self.wdg_resolution.set_boundry(min,max,value)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Horizontal_Toolbar(QToolBar):

    def __init__(self):

        QToolBar.__init__(self)
        self.setOrientation(Qt.Horizontal)

        self.wdg_refresh    = MQT_WDG_Button(MQT_ICON("refresh"),  MQT_ICON("refresh_hover"),  "Refresh Image")
        self.wdg_snapshot   = MQT_WDG_Button(MQT_ICON("snapshot"), MQT_ICON("snapshot_hover"), "Save Image")
        self.wdg_default    = MQT_WDG_Button(MQT_ICON("default"), MQT_ICON("default_hover"),   "Return to Default")
        self.wdg_set        = MQT_WDG_Selection()
        self.wdg_set.setFixedWidth(160)


        self.wdg_custom_power  = MQT_WDG_Input("z power = ")
        self.wdg_custom_power.spin.setValue(2.0)
        self.wdg_custom_power.spin.setMinimum(-10000)
        self.wdg_custom_c_real = MQT_WDG_Input("Re(c) = ")        
        self.wdg_custom_c_real.spin.setMinimum(-10000)
        self.wdg_custom_c_real.spin.setValue(-0.1)
        self.wdg_custom_c_imag = MQT_WDG_Input("Im(c) = ")
        self.wdg_custom_c_imag.spin.setValue(0.65)
        self.wdg_custom_c_imag.spin.setMinimum(-10000)

        self.wdg_formula = QLabel()


        self.addWidget(self.wdg_refresh)
        self.addWidget(self.wdg_snapshot)
        self.addWidget(self.wdg_default)
        self.addSeparator()
        self.addWidget(self.wdg_set)
        self.addSeparator()
        self.addWidget(self.wdg_formula)
        self.addSeparator()
        self.addWidget(self.wdg_custom_power)
        self.addWidget(self.wdg_custom_c_real)
        self.addWidget(self.wdg_custom_c_imag)

        self.custom_input_visibility(False)

        self.wdg_set.populate(CST_SETS)

    def register_refresh_clbk(self,clbk):

        self.wdg_refresh.register_button_clbk(clbk)

    def register_snapshot_clbk(self,clbk):

        self.wdg_snapshot.register_button_clbk(clbk)

    def register_default_clbk(self,clbk):

        self.wdg_default.register_button_clbk(clbk)

    def register_set_clbk(self,clbk):

        self.wdg_set.register_change(clbk)

    def register_custom_power_clbk(self,clbk):

        self.wdg_custom_power.register_clbk(clbk)
        
    def register_custom_imag_c_clbk(self,clbk):

        self.wdg_custom_c_imag.register_clbk(clbk)

    def register_custom_real_c_clbk(self,clbk):

        self.wdg_custom_c_real.register_clbk(clbk)

    def custom_input_visibility(self,status):

        self.wdg_custom_power.set_visibility(status)
        self.wdg_custom_c_real.set_visibility(status)
        self.wdg_custom_c_imag.set_visibility(status)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Slider(QSlider):

    def __init__(self,label):

        QSlider.__init__(self,orientation=Qt.Vertical)

        self.setTickPosition(QSlider.NoTicks)
        self.setMinimumSize(20, 700)
        self.setTickInterval(1)
        self.setMaximum(CST_RESOLUTION_1_MAX)
        self.setMinimum(CST_RESOLUTION_1_MIN)
        self.setValue(CST_RESOLUTION_1_DEFAULT)

    def register_value_changed(self,clbk):

        self.valueChanged.connect(clbk)

    def set_boundry(self,min,max,value):

        self.setMaximum(max)
        self.setMinimum(min)
        self.setValue(value)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_DrawArea(object):

    def __init__(self):

        self.scene = QGraphicsScene()
        self.view  = QGraphicsView(self.scene)
        self.image = None

        self.scene.mousePressEvent   = self.mousePressEvent
        self.scene.mouseReleaseEvent = self.mouseReleaseEvent
        self.scene.mouseMoveEvent    = self.mouseMoveEvent

        self.rubber_band = None
        self.start_point = None
        self.end_point   = None

        self.use_rubber_band = False

        self.rubber_band =  QRubberBand(QRubberBand.Rectangle,self.view)

        self.mouse_move_clbk = None

    def draw_images(self,image,pixmap):

        if self.rubber_band:
            self.rubber_band.hide()

        self.image = image

        self.pixmap = pixmap

        self.scene.addPixmap(self.pixmap);

    def __get_image_path(self):

        _path = os.path.split(__file__)[0]

        _path = os.path.join(_path,strftime("img_%d_%m_%Y_%H_%M_%S.png", gmtime()))

        return _path

    def snapshot(self):

        _path = self.__get_image_path()

        if self.image:

            self.image.save(_path,"PNG")

            os.system(_path)

    def register_mouse_move_clbk(self,clbk):

        self.mouse_move_clbk = clbk

    def mousePressEvent(self,event):

        if self.use_rubber_band:

            self.start_point = event.scenePos().toPoint()

            self.rubber_band.hide()
            self.rubber_band.show()

    def mouseMoveEvent(self,event):

        _offset = QPoint(CST_SCENE_OFFSET_X,CST_SCENE_OFFSET_Y)

        if self.use_rubber_band:

            _crt_point = event.scenePos().toPoint()

            self.rubber_band.setGeometry(QRect(self.start_point + _offset, _crt_point + _offset).normalized())

            self.mouse_move_clbk(_crt_point)
        
    def mouseReleaseEvent(self,event):

        if self.use_rubber_band:

            self.end_point = event.scenePos().toPoint()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_StatusBar(QStatusBar):

    def __init__(self):

        QStatusBar.__init__(self)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setValue(0)

        self.addPermanentWidget(self.progress, 2 )

    def set_progress(self,value):

        self.progress.setValue(value)
        QApplication.instance().processEvents()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Selection(QComboBox):

    def __init__(self):

        QComboBox.__init__(self)

        _css  = """ background-color: %s;
                     color: #000000;  
                     border: %spx solid gray;
                     border-color: %s;
                     border-radius: %spx;
                     """ % ("#FFFFFF","1","#838487","2")


        self.setStyleSheet(_css)
        self.editTextChanged.connect(self.textChangedHandler)
        self.setEditable(True)
        self.data = []
        self._model_items = []

    def __create_completer(self):

        self.completer = QCompleter()

        self.completer.setFilterMode(Qt.MatchContains)

        self.setCompleter(self.completer)        

        self.model = QStringListModel()

        self.completer.setModel(self.model)        

        self._model_items = [list(_item.keys())[0] for _item in self.data]

        self.model.setStringList(self._model_items)

        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionRole(Qt.DisplayRole)

    def populate(self,data):

        self.data = data

        self.clear()
        for _item in self.data:

            self.addItem(list(_item.keys())[0])

        self.__create_completer()

        self.setCurrentIndex(0)

    def get_item_data(self,text):

        _data = ""

        for _index in range(len(self.data)):

            if list(self.data[_index].keys())[0] == text:

                _data = self.data[_index][list(self.data[_index].keys())[0]]
        
        return _data

    def textChangedHandler(self, text):

        if self._model_items:
            if str(text) in self._model_items or not len(text):
                self.setStyleSheet("background-color: white; border: %spx solid gray;" % "1")
            else: 
                self.setStyleSheet("background-color: #ffcccc; border: %spx solid gray;" % "1")

    def register_change(self,clbk):

        self.currentIndexChanged.connect(clbk)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Input(QWidget):

    def __init__(self,label):

        QWidget.__init__(self)

        self.label = QLabel(label)
        self.spin  = QDoubleSpinBox()


        self.ly = QHBoxLayout()

        self.ly.addWidget(self.label)
        self.ly.addWidget(self.spin)

        self.setLayout(self.ly)

    def set_visibility(self,status):

        if status:

            self.label.show()
            self.spin.show()
            self.show()
        else:

            self.label.hide()
            self.spin.hide()
            self.hide()

    def value(self):

        return self.spin.value()

    def register_clbk(self,clbk):

        self.spin.valueChanged.connect(clbk)

