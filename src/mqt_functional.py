
from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import * 

from mqt_constants    import *

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _MQT_Functional_Base(object):

    def __init__(self):

        self.max_iteration = CST_RESOLUTION_DEFAULT
        self.height        = CST_IMAGE_HEIGHT    
        self.width         = CST_IMAGE_WIDTH

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
        _re_offset     = (x / self.width)  * (self.re_end - self.re_start)
        _im_offset     = (y / self.height) * (self.im_end - self.im_start)

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
                                int(255 * _value / self.max_iteration),
                                CST_DEFAULT_SATURATION,
                                255 if _value < self.max_iteration else 0,
                                c])

                observer.set_progress((100.0/float(_prg_total)) * _prg_crt)

                _prg_crt += 1

        return _pixels

    def set_default(self):

        self.re_start      = -2
        self.re_end        = 1

        self.im_start      = -1
        self.im_end        = 1

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_Functional_Julia(_MQT_Functional_Base):

    def __init__(self):

        _MQT_Functional_Base.__init__(self)

        self.max_iteration = 100
        self.limit         = 10
        self.re_start      = -1.5
        self.re_end        = 1.5
        self.im_start      = -1.5
        self.im_end        = 1.5

    def __get_julia_value(self,x,y):

        _crt_iteration = 0
        _re_offset = (x / self.width)  * (self.re_end - self.re_start)
        _im_offset = (y / self.height) * (self.im_end - self.im_start)

        z = complex(self.re_start + _re_offset, self.im_start + _im_offset)
        c = complex(-0.1, 0.65)

        while abs(z) <= self.limit and _crt_iteration < self.max_iteration:

            z = z * z + c

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
                                int(255 * _value / self.max_iteration),
                                CST_DEFAULT_SATURATION,
                                255 if _value < self.max_iteration else 0,
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

        self.re_start      = -2
        self.re_end        = 1

        self.im_start      = -1
        self.im_end        = 1