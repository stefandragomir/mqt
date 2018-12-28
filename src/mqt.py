
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
from mqt_functional   import MQT_Functional_Mandelbrot

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class MQT(MQT_WDG_Window):

    def __init__(self):

        MQT_WDG_Window.__init__(self)

        self.pixels     = []
        self.functional = MQT_Functional_Mandelbrot()

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
        self.wdg_htoolbar.register_default_clbk(self.clbk_default)
        self.wdg_htoolbar.register_set_clbk(self.clbk_set)

    def draw_image(self):

        if self.functional:

            self.get_roi()

            self.pixels = self.functional.get_pixel_values(self.status)

            self.wdg_area.draw_images(self.pixels)

            self.status.set_progress(0)

    def get_roi(self):

        if self.wdg_area.start_point and self.wdg_area.end_point:

            _start_x = self.wdg_area.start_point.x()
            _start_y = self.wdg_area.start_point.y()
            _end_x   = self.wdg_area.end_point.x()
            _end_y   = self.wdg_area.end_point.y()

            _start_pixel = self.find_pixel(_start_x, _start_y)
            _end_pixel   = self.find_pixel(_end_x  , _end_y)

            if _start_pixel and _end_pixel:

                self.functional.re_start = _start_pixel[5].real
                self.functional.re_end   = _end_pixel[5].real

                self.functional.im_start = _start_pixel[5].imag
                self.functional.im_end   = _end_pixel[5].imag

    def find_pixel(self,x,y):

        _the_pixel = None

        for _pixel in self.pixels:

            if _pixel[0] == x and _pixel[1] == y:

                _the_pixel = _pixel

        return _the_pixel

    def clbk_resolution(self,resolution):

        self.functional.max_iteration = resolution

    def clbk_refresh(self):

        self.draw_image()

    def clbk_snapshot(self):

        self.wdg_area.snapshot()

    def clbk_set(self,index):

        _crt_set = self.wdg_htoolbar.wdg_set.currentText()

        if _crt_set in [list(_set.keys())[0] for _set in CST_SETS]:

            if _crt_set == "Mandelbrot":

                self.functional = MQT_Functional_Mandelbrot()
        else:
            self.set = None

    def clbk_default(self):

        self.wdg_area.start_point = None
        self.wdg_area.end_point   = None

        if self.functional:
            self.functional.set_default()

            self.draw_image()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = MQT()   

    sys.exit(_app.exec_())
