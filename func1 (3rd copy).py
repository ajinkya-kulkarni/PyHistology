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

def create_HSV_mask(image, lower_value, upper_value):
    """
    This function takes an RGB image and creates an HSV mask based on the given lower and upper value.
    The function returns the output_HSV_image and mask.
    
    Parameters:
    - image (ndarray): The input RGB image.
    - lower_value (tuple): The lower value of the color range for creating the mask.
    - upper_value (tuple): The upper value of the color range for creating the mask.
    
    Returns:
    - output_HSV_image (ndarray): The output HSV image after applying the mask.
    - mask (ndarray): The created mask.
    """
    if len(image.shape) != 3:
        raise ValueError("Input image should be a 3 channel RGB image")
    if len(lower_value) != 3 or len(upper_value) != 3:
        raise ValueError("lower_value and upper_value should be a tuple of 3 elements (H, S, V)")
    HSV_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(HSV_image, lower_value, upper_value)
    output_HSV_image = cv2.bitwise_and(HSV_image, HSV_image, mask = mask)
    return output_HSV_image, mask
