
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

    def __get_mandelbrot_value(self,c):
        """
        Calculate Mandelbrot Set

        z(n+1) = z(n) * z(n) + c

        * we return the number of iteration needed by the mandelbrot formula to reach the limit value
        * see https://en.wikipedia.org/wiki/Mandelbrot_set

        """

        z = 0
        _crt_iteration = 0

        while abs(z) <= self.limit and _crt_iteration < self.max_iteration:

            z = z * z + c

            _crt_iteration += 1

        return _crt_iteration

    def __get_constant(self,x,y):

        _re_offset = (x / self.width)  * (self.re_end - self.re_start)
        _im_offset = (y / self.height) * (self.im_end - self.im_start)

        _cst = complex(self.re_start + _re_offset, self.im_start + _im_offset)

        return _cst

    def draw(self,observer):

        _pixels = self.__get_pixel_values(observer)

        _image = QImage(CST_IMAGE_WIDTH, CST_IMAGE_HEIGHT, QImage.Format_RGB32)

        for _pixel in _pixels:

            _color = QColor()
            _color.setHsv(_pixel[2], _pixel[3], _pixel[4], 0xFF)

            _image.setPixelColor(_pixel[0], _pixel[1], _color)

        _pixmap = QPixmap.fromImage(_image)

        return _image,_pixmap

    def __get_pixel_values(self,observer):

        _pixels = []

        _prg_total = self.width * self.height
        _prg_crt   = 0

        for x in range(0, self.width):

            for y in range(0, self.height):

                _cst              = self.__get_constant(x,y)
                _mandelbrot_value = self.__get_mandelbrot_value(_cst)

                _hue        = int(255 * _mandelbrot_value / self.max_iteration)
                _saturation = CST_DEFAULT_SATURATION
                _value      = 255 if _mandelbrot_value < self.max_iteration else 0

                _pixels.append([
                                x,
                                y,
                                _hue,
                                _saturation,
                                _value,
                                _cst])

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

        self.limit    = 10
        self.re_start = -1.5
        self.re_end   = 1.5
        self.im_start = -1.5
        self.im_end   = 1.5
        self.constant = complex(-0.1, 0.65)

    def __get_julia_value(self,c):
        """
        Calculate Mandelbrot Set

        z(n+1) = z(n) * z(n) + c

        * we return the number of iteration needed by the mandelbrot formula to reach the limit value
        * see https://en.wikipedia.org/wiki/Mandelbrot_set

        """

        z = 0
        _crt_iteration = 0

        while abs(z) <= self.limit and _crt_iteration < self.max_iteration:

            z = z * z + self.constant

            _crt_iteration += 1

        # _shade = 1 - np.sqrt(_crt_iteration / self.max_iteration)
        _ratio = _crt_iteration / self.max_iteration

        return _ratio

    def __get_z(self,x,y):

        _re_offset = (x / self.width)  * (self.re_end - self.re_start)
        _im_offset = (y / self.height) * (self.im_end - self.im_start)

        _z = complex(self.re_start + _re_offset, self.im_start + _im_offset)

        return _z

    def __get_pixel_values(self,observer):

        _pixels = []

        _prg_total = self.width * self.height
        _prg_crt   = 0

        for x in range(0, self.width):

            for y in range(0, self.height):

                _z           = self.__get_z(x,y)
                _julia_value = self.__get_julia_value(_z)

                _hue        = int(255 * _julia_value / self.max_iteration)
                _saturation = CST_DEFAULT_SATURATION
                _value      = 255 if _julia_value < self.max_iteration else 0

                _pixels.append([
                                x,
                                y,
                                _hue,
                                _saturation,
                                _value,
                                _z])

                observer.set_progress((100.0/float(_prg_total)) * _prg_crt)

                _prg_crt += 1

        return _pixels

    def set_default(self):

        self.re_start      = -2
        self.re_end        = 1

        self.im_start      = -1
        self.im_end        = 1