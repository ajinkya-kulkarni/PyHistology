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

from matplotlib.colors import hex2color
import numpy as np

def hex_to_rgb(hexcode):
	"""
	Convert hex color code to RGB color values.

	Parameters:
	hexcode (str): Hex color code string in the format of "#RRGGBB"

	Returns:
	np.ndarray: RGB color values as integers in the format of [R, G, B]

	Raises:
	TypeError: If input is not a string
	ValueError: If input string is not in the format of "#RRGGBB"
	"""
	if not isinstance(hexcode, str):
		raise TypeError("Input must be a string")
	if not hexcode.startswith("#") or len(hexcode) != 7:
		raise ValueError("Invalid hexcode format, should be in the format of '#RRGGBB'")

	# Convert hexcode to RGB color values using matplotlib hex2color function
	rgb_color_raw = np.asarray(hex2color(hexcode))

	# Multiply by 255 to get RGB values in the range of 0-255
	rgb_color = np.rint(255 * rgb_color_raw).astype(int)

	return rgb_color