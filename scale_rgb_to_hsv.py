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

#######################################################################################################

from matplotlib.colors import rgb_to_hsv
from PIL import ImageColor

def scale_rgb_to_hsv(color:str):
    # Get the RGB values of the color
    rgb = ImageColor.getrgb(color)

    # Convert the RGB values to HSV values
    hsv = rgb_to_hsv(rgb)

    # Scale the H, S, and V values
    h = int(hsv[0] * 360)
    s = int(hsv[1] * 255)
    v = int(hsv[2])

    # Return the scaled HSV values
    return (h, s, v)
