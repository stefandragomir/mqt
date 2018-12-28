
import math

from mqt_constants    import *

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class MQT_Functional(object):

    def __init__(self):

        self.set = "Mandelbrot"

        self.max_iteration = CST_RESOLUTION_DEFAULT

        self.height        = CST_IMAGE_HEIGHT    
        self.width         = CST_IMAGE_WIDTH

    def get_pixel_values(self):

        _pixels = []

        if self.set == "Mandelbrot":

            _set = _MQT_Functional_Mandelbrot(self.max_iteration,self.height,self.width)

            _pixels = _set.get_pixel_values()
        else:
            if self.set == "Julia":

                pass


        return _pixels

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _MQT_Functional_Mandelbrot(object):

    def __init__(self,max_iteration,height,width):

        self.max_iteration = max_iteration

        self.height        = height    
        self.width         = width

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

    def __get_pixel_coordinates(self,x,y):

        _coordinates = complex(
                                self.re_start + (x / self.width) * (self.re_end - self.re_start),
                                self.im_start + (y / self.height) * (self.im_end - self.im_start)
                                )

        return _coordinates

    def get_pixel_values(self):

        _pixels = []

        for x in range(0, self.width):

            for y in range(0, self.height):

                _coordinates      = self.__get_pixel_coordinates(x,y)
                _mandelbrot_value = self.__get_mandelbrot_value(_coordinates)

                _hue        = int(255 * _mandelbrot_value / self.max_iteration)
                _saturation = CST_DEFAULT_SATURATION
                _value      = 255 if _mandelbrot_value < self.max_iteration else 0

                _pixels.append([x,y,_hue,_saturation,_value])

        return _pixels

"""****************************************************************************
*******************************************************************************
****************************************************************************"""