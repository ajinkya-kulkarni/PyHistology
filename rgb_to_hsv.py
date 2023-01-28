#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (C) 2022 Max Planck Institute for Multidisclplinary Sciences
# Copyright (C) 2022 University Medical Center Goettingen
# Copyright (C) 2022 Ajinkya Kulkarni <ajinkya.kulkarni@mpinat.mpg.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

########################################################################################

import cv2
import numpy as np

def rgb_to_hsv(array):
	"""
	Convert RGB color to HSV color.

	Parameters:
	array (list or numpy.ndarray): RGB values of the color in the format [R, G, B].

	Returns:
	numpy.ndarray: HSV values of the color in the format [H, S, V].
	"""
	if not isinstance(array, (list, np.ndarray)):
		raise TypeError("Input must be a list or numpy array")
	if len(array) != 3:
		raise ValueError("Invalid RGB array format")

	# Convert RGB to HSV
	rgb = np.array([[array]], dtype = np.uint8)
	hsv_raw = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

	#squeeze the array and round it to nearest int
	hsv_color = np.rint(hsv_raw.squeeze()).astype(int)

	return hsv_color