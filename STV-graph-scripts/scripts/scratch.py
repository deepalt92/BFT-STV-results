#!/usr/bin/env python

import numpy as np

data = [1, 2, 3, 4]
kernel_size = 2
kernel = np.ones(kernel_size) / kernel_size
data_convolved_2 = np.convolve(data, kernel, mode='same')
print(data_convolved_2)
