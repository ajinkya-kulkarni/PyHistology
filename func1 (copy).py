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

def count_nonwhite_pixels(image_gray, whiteness_threshold):
    """
    This function counts the number of non-white pixels in a grayscale image.
    The function returns the number of non-white pixels.

    Parameters:
    - image_gray (ndarray): The input grayscale image.
    - whiteness_threshold (int): The threshold value for determining white pixels.
    
    Returns:
    - non_white_pixels (int): The number of non-white pixels in the image.
    """
    if len(image_gray.shape) != 2:
        raise ValueError("Input image should be a 2 channel grayscale image")
    if not isinstance(whiteness_threshold, int):
        raise ValueError("whiteness_threshold should be an integer.")
    non_white_pixels = np.count_nonzero(image_gray < whiteness_threshold)
    return non_white_pixels
