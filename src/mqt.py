
import sys

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import * 
from mqt_constants    import *
from mqt_widgets      import MQT_WDG_Slider
from mqt_widgets      import MQT_WDG_Window
from mqt_widgets      import MQT_WDG_Vertical_Toolbar
from mqt_widgets      import MQT_WDG_Horizontal_Toolbar
from mqt_widgets      import MQT_WDG_DrawArea
from mqt_functional   import MQT_Functional

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class MQT(MQT_WDG_Window):

    def __init__(self):

        MQT_WDG_Window.__init__(self)

        self.functional = MQT_Functional()

        self.draw() 

        self.show()        

    def draw(self):

        self.wdg_vtoolbar = MQT_WDG_Vertical_Toolbar()
        self.wdg_htoolbar = MQT_WDG_Horizontal_Toolbar()
        self.wdg_area     = MQT_WDG_DrawArea()
        self.wdg_central  = QWidget()

        self.ly_top    = QHBoxLayout()
        self.ly_top.addWidget(self.wdg_htoolbar)

        self.ly_bottom = QHBoxLayout()
        self.ly_bottom.addWidget(self.wdg_area.view)
        self.ly_bottom.addWidget(self.wdg_vtoolbar)
       
        self.ly_main = QVBoxLayout()
        self.ly_main.addLayout(self.ly_top)
        self.ly_main.addLayout(self.ly_bottom)
        
        self.wdg_central.setLayout(self.ly_main)  

        self.setCentralWidget(self.wdg_central)

        self.activateWindow() 

        self.wdg_vtoolbar.register_resolution_clbk(self.clbk_resolution)
        self.wdg_htoolbar.register_refresh_clbk(self.clbk_refresh)
        self.wdg_htoolbar.register_snapshot_clbk(self.clbk_snapshot)
        self.wdg_htoolbar.register_set_clbk(self.clbk_set)

    def draw_image(self):

        self.status.showMessage("Calculating Values ... ")

        _pixels = self.functional.get_pixel_values()

        self.status.showMessage("Drawing Image ... ")

        self.wdg_area.draw_images(_pixels)

        self.status.showMessage("Done")

    def clbk_resolution(self,resolution):

        self.functional.max_iteration = resolution

    def clbk_refresh(self):

        self.draw_image()

    def clbk_snapshot(self):

        self.wdg_area.snapshot()

    def clbk_set(self,index):

        _crt_set = self.wdg_htoolbar.wdg_set.currentText()

        if _crt_set in [list(_set.keys())[0] for _set in CST_SETS]:

            self.functional.set = _crt_set
        else:
            self.functional.set = None

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = MQT()   

    sys.exit(_app.exec_())
