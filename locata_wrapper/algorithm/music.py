# -*- coding: utf-8 -*-
import numpy as np


class MUSIC(object):
    """docstring for MUSIC"""

    def __init__(self, arg):
        super(MUSIC, self).__init__()
        self.arg = arg
        self.value = np.random.randn(10, 10)
