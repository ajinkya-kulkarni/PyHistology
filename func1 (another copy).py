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

def create_grayscale_image(image):
    """
    This function converts a RGB image to grayscale image
    The function returns the grayscale image.

    Parameters:
    - image (ndarray): The input RGB image.
    
    Returns:
    - image_gray (ndarray): The output grayscale image
    """
    if len(image.shape) != 3:
        raise ValueError("Input image should be a 3 channel RGB image")
    image_gray = 255 * rgb2gray(image)
    return image_gray

