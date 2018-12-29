import sys
from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import * 

from mqt_constants    import *

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _MQT_Functional_Base(object):

    def __init__(self):

        self.color_base    = "Blue"

        self.max_iteration = CST_RESOLUTION_1_DEFAULT
        self.height        = CST_IMAGE_HEIGHT    
        self.width         = CST_IMAGE_WIDTH

    def get_pixel_color_saturation(self,set_value):

        return CST_DEFAULT_SATURATION

    def get_pixel_color_hue(self,set_value):

        _offset = 200

        if self.color_base == "Orange":
            _offset = 0
        elif self.color_base == "Yellow":
            _offset = 50
        elif self.color_base == "Green":
            _offset = 100
        elif self.color_base == "Light Green":
            _offset = 150
        elif self.color_base == "Blue":
            _offset = 200
        elif self.color_base == "High Contrast":
            _offset = 220

        return (int(255 * (set_value / self.max_iteration)) + _offset) % 255

    def get_pixel_color_value(self,set_value):

        if self.color_base == "Dark":

            _value = int(255 * (set_value / self.max_iteration))
        else:
            _value = 255 if set_value < self.max_iteration else 0

        return _value

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_Functional_Mandelbrot(_MQT_Functional_Base):

    def __init__(self):

        _MQT_Functional_Base.__init__(self)

        self.limit         = 2
        self.re_start      = -2
        self.re_end        = 1
        self.im_start      = -1
        self.im_end        = 1

    def __get_mandelbrot_value(self,x,y):

        z              = 0
        _crt_iteration = 0
        _re_offset     = (float(x) / float(self.width))  * (float(self.re_end) - float(self.re_start))
        _im_offset     = (float(y) / float(self.height)) * (float(self.im_end) - float(self.im_start))

        c = complex(self.re_start + _re_offset, self.im_start + _im_offset)

        while abs(z) <= self.limit and _crt_iteration < self.max_iteration:

            z = z * z + c 

            _crt_iteration += 1

        return _crt_iteration,c

    def draw(self,observer):

        _pixels = self.__get_pixel_values(observer)

        _image = QImage(CST_IMAGE_WIDTH, CST_IMAGE_HEIGHT, QImage.Format_RGB32)

        for _pixel in _pixels:

            _color = QColor()
            _color.setHsv(_pixel[2], _pixel[3], _pixel[4], 0xFF)

            _image.setPixelColor(_pixel[0], _pixel[1], _color)

        _pixmap = QPixmap.fromImage(_image)

        return _image,_pixmap,_pixels

    def __get_pixel_values(self,observer):

        _pixels = []

        _prg_total = self.width * self.height
        _prg_crt   = 0

        for x in range(0, self.width):

            for y in range(0, self.height):

                _value,c = self.__get_mandelbrot_value(x,y)

                _pixels.append([
                                x,
                                y,
                                self.get_pixel_color_hue(_value),
                                self.get_pixel_color_saturation(_value),
                                self.get_pixel_color_value(_value),
                                c])

                observer.set_progress((100.0/float(_prg_total)) * _prg_crt)

                _prg_crt += 1

        return _pixels

    def set_default(self):

        self.limit         = 2
        self.re_start      = -2
        self.re_end        = 1
        self.im_start      = -1
        self.im_end        = 1

    def formula_text(self):

        return "f(z) = pow(z,2) + c with lim(f(z)) <= 2 and %s iterations" % (self.max_iteration)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_Functional_Julia(_MQT_Functional_Base):

    def __init__(self,power=2,real_c=-0.1,imag_c=0.65):

        _MQT_Functional_Base.__init__(self)

        self.max_iteration = 1000
        self.limit         = 10
        self.re_start      = -1.5
        self.re_end        = 1.5
        self.im_start      = -1.5
        self.im_end        = 1.5

        self.power  = power
        self.real_c = real_c
        self.imag_c = imag_c

    def __get_julia_value(self,x,y):

        _crt_iteration = 0
        _re_offset = (x / self.width)  * (self.re_end - self.re_start)
        _im_offset = (y / self.height) * (self.im_end - self.im_start)

        z = complex(self.re_start + _re_offset, self.im_start + _im_offset)
        z_init = z
        c = complex(self.real_c, self.imag_c)

        while abs(z) <= self.limit and _crt_iteration < self.max_iteration:

            z = z**self.power + c

            _crt_iteration += 1

        return _crt_iteration,z

    def __get_pixel_values(self,observer):

        _pixels = []

        _prg_total = self.width * self.height
        _prg_crt   = 0

        for x in range(0, self.width):

            for y in range(0, self.height):

                _value,_z = self.__get_julia_value(x,y)

                _pixels.append([
                                x,
                                y,
                                self.get_pixel_color_hue(_value),
                                self.get_pixel_color_saturation(_value),
                                self.get_pixel_color_value(_value),
                                _z])

                observer.set_progress((100.0/float(_prg_total)) * _prg_crt)

                _prg_crt += 1

        return _pixels

    def draw(self,observer):

        _pixels = self.__get_pixel_values(observer)

        _image = QImage(CST_IMAGE_WIDTH, CST_IMAGE_HEIGHT, QImage.Format_RGB32)

        for _pixel in _pixels:

            _color = QColor()
            _color.setHsv(_pixel[2], _pixel[3], _pixel[4], 0xFF)

            _image.setPixelColor(_pixel[0], _pixel[1], _color)

        _pixmap = QPixmap.fromImage(_image)

        return _image,_pixmap,_pixels

    def set_default(self):

        self.max_iteration = 1000
        self.limit         = 10
        self.re_start      = -1.5
        self.re_end        = 1.5
        self.im_start      = -1.5
        self.im_end        = 1.5

    def formula_text(self):

        return "f(z) = pow(z,%s) + (%s + %si) with lim(f(z)) <= %s and %s iterations" % (self.power,self.real_c,self.imag_c,self.limit,self.max_iteration)

