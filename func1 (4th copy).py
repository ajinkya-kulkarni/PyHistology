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

def convert_HSV_to_RGB(output_HSV_image, mask):
    """
    This function convert HSV image to RGB image and counts the number of blue pixels in the image
    The function returns the RGB image, number of blue pixels.

    Parameters:
    - output_HSV_image (ndarray): The input HSV image.
    - mask (ndarray): The binary image used to count number of blue pixels in the image.
    
    Returns:
    - output_RGB_image (ndarray): The output RGB image.
    - blue_pixels (int): The number of blue pixels in the image.
    """
    if len(output_HSV_image.shape) != 3:
        raise ValueError("Input image should be a 3 channel HSV image")
    if mask.shape != output_HSV_image.shape[:2]:
        raise ValueError("mask should have the same shape as the image.")
    output_RGB_image = cv2.cvtColor(output_HSV_image, cv2.COLOR_HSV2RGB)
    blue_pixels = np.count_nonzero(mask)
    return output_RGB_image, blue_pixels
