
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
from mqt_functional   import MQT_Functional_Julia

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
        self.color_base   = "Blue"

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
        self.wdg_htoolbar.register_color_base_clbk(self.clbk_color_base)
        self.wdg_area.register_mouse_move_clbk(self.clbk_mouse_move)
        self.wdg_htoolbar.register_custom_power_clbk(self.clbk_custom_power)
        self.wdg_htoolbar.register_custom_imag_c_clbk(self.clbk_custom_imag_c)
        self.wdg_htoolbar.register_custom_real_c_clbk(self.clbk_custom_real_c)

        self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())

    def draw_image(self):
        
        self.wdg_area.use_rubber_band = True

        if self.functional:

            self.wdg_area.use_rubber_band = False

            self.get_roi()

            _image,_pixmap,self.pixels = self.functional.draw(self.status)

            self.wdg_area.draw_images(_image,_pixmap)

            self.status.set_progress(0)

            self.wdg_area.rubber_band.hide()

            self.wdg_area.use_rubber_band = True

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

    def clbk_mouse_move(self,point):

        pass

        #print(point)

    def clbk_resolution(self,resolution):

        self.functional.max_iteration = resolution

        self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())

    def clbk_refresh(self):

        self.draw_image()

    def clbk_snapshot(self):

        self.wdg_area.snapshot()

    def clbk_color_base(self,index):

         _crt_color_base = self.wdg_htoolbar.wdg_color_base.currentText()

         if _crt_color_base in [list(_color_base.keys())[0] for _color_base in CST_COLOR_BASE]:

            self.functional.color_base = _crt_color_base

    def clbk_set(self,index):

        _crt_set = self.wdg_htoolbar.wdg_set.currentText()

        if _crt_set in [list(_set.keys())[0] for _set in CST_SETS]:

            if _crt_set == "Mandelbrot":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_1_MIN,CST_RESOLUTION_1_MAX,CST_RESOLUTION_1_DEFAULT)
                self.functional = MQT_Functional_Mandelbrot()
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())

            elif _crt_set == "Julia":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia()
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())

            elif _crt_set == "Julia Custom 1":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=1-CST_GOLDEN_RATIO,imag_c=0)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())

            elif _crt_set == "Julia Custom 2":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=CST_GOLDEN_RATIO-2,imag_c=CST_GOLDEN_RATIO-1)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 3":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=0.285,imag_c=0)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 4":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=0.285,imag_c=0.01)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 5":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=0.45,imag_c=0.1428)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 6":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=-0.70176,imag_c=-0.3842)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 7":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=-0.835,imag_c=-0.2321)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 8":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=-0.8,imag_c=-0.156)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 9":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=-0.7269,imag_c=0.1889)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 10":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=0,imag_c=-0.8)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 11":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=2,real_c=0.279,imag_c=0)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 12":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=3,real_c=0.400,imag_c=0)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 13":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=4,real_c=0.484,imag_c=0)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Julia Custom 14":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia(power=4,real_c=0.626)
                self.wdg_htoolbar.custom_input_visibility(False)
                self.wdg_htoolbar.wdg_formula.setText(self.functional.formula_text())


            elif _crt_set == "Custom Julia":

                self.wdg_vtoolbar.set_resolution_boundry(CST_RESOLUTION_2_MIN,CST_RESOLUTION_2_MAX,CST_RESOLUTION_2_DEFAULT)
                self.functional = MQT_Functional_Julia()
                self.wdg_htoolbar.custom_input_visibility(True)
                self.wdg_htoolbar.wdg_formula.setText("")

            self.functional.color_base = self.color_base

        else:
            self.set = None

    def clbk_default(self):

        self.wdg_area.start_point = None
        self.wdg_area.end_point   = None

        if self.functional:
            self.functional.set_default()

            self.draw_image()

    def clbk_custom_power(self,value):

        self.functional.power  = value

    def clbk_custom_imag_c(self,value):

        self.functional.imag_c  = value

    def clbk_custom_real_c(self,value):

        self.functional.real_c = value


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = MQT()   

    sys.exit(_app.exec_())
