
import math

from mqt_constants    import *


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_Functional_Mandelbrot(object):

    def __init__(self):

        self.limit         = 2
        self.max_iteration = CST_RESOLUTION_DEFAULT
        self.height        = CST_IMAGE_HEIGHT    
        self.width         = CST_IMAGE_WIDTH

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

    def get_pixel_values(self,observer):

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