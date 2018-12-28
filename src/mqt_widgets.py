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

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Horizontal_Toolbar(QToolBar):

    def __init__(self):

        QToolBar.__init__(self)
        self.setOrientation(Qt.Horizontal)

        self.wdg_refresh    = MQT_WDG_Button(MQT_ICON("refresh"),  MQT_ICON("refresh_hover"),  "Refresh Image")
        self.wdg_snapshot   = MQT_WDG_Button(MQT_ICON("snapshot"), MQT_ICON("snapshot_hover"), "Save Image")
        self.wdg_set        = MQT_WDG_Selection()
        self.wdg_set.setFixedWidth(110)
        


        self.addWidget(self.wdg_refresh)
        self.addWidget(self.wdg_snapshot)
        self.addSeparator()
        self.addWidget(self.wdg_set)

        self.wdg_set.populate(CST_SETS)

    def register_refresh_clbk(self,clbk):

        self.wdg_refresh.register_button_clbk(clbk)

    def register_snapshot_clbk(self,clbk):

        self.wdg_snapshot.register_button_clbk(clbk)

    def register_set_clbk(self,clbk):

        self.wdg_set.register_change(clbk)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_Slider(QSlider):

    def __init__(self,label):

        QSlider.__init__(self,orientation=Qt.Vertical)

        self.setTickPosition(QSlider.NoTicks)
        self.setMinimumSize(20, 700)
        self.setTickInterval(1)
        self.setMaximum(CST_RESOLUTION_MAX)
        self.setMinimum(CST_RESOLUTION_MIN)
        self.setValue(CST_RESOLUTION_DEFAULT)

    def register_value_changed(self,clbk):

        self.valueChanged.connect(clbk)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_DrawArea(object):

    def __init__(self):

        self.scene = QGraphicsScene()
        self.view  = QGraphicsView(self.scene)
        self.image = None

    def draw_images(self,hsv_pixels):

        self.image = QImage(CST_IMAGE_WIDTH, CST_IMAGE_HEIGHT, QImage.Format_RGB32)

        for _pixel in hsv_pixels:

            _color = QColor()
            _color.setHsv(_pixel[2], _pixel[3], _pixel[4], 0xFF)

            self.image.setPixelColor(_pixel[0], _pixel[1], _color)

        self.pixmap = QPixmap.fromImage(self.image)

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

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_WDG_StatusBar(QStatusBar):

    def __init__(self):

        QStatusBar.__init__(self)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
_WDG_BACK_COLOR    = "#FFFFFF"
_WDG_BORDER_COLOR  = "#838487"
_WDG_BORDER_WIDTH  = "1"
_WDG_BORDER_RADIUS = "2"

class MQT_WDG_Selection(QComboBox):

    def __init__(self):

        QComboBox.__init__(self)

        _css  = """ background-color: %s;
                     color: #000000;  
                     border: %spx solid gray;
                     border-color: %s;
                     border-radius: %spx;
                     """ % (_WDG_BACK_COLOR,_WDG_BORDER_WIDTH,_WDG_BORDER_COLOR,_WDG_BORDER_RADIUS)


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
                self.setStyleSheet("background-color: white; border: %spx solid gray;" % _WDG_BORDER_WIDTH)
            else: 
                self.setStyleSheet("background-color: #ffcccc; border: %spx solid gray;" % _WDG_BORDER_WIDTH)

    def register_change(self,clbk):

        self.currentIndexChanged.connect(clbk)