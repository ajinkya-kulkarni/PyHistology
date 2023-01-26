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

def read_image(filename):
    """
    This function reads an image from a file and converts it from BGR to RGB color space
    The function returns the RGB image.

    Parameters:
    - filename (str): The path of the image file.
    
    Returns:
    - image (ndarray): The output RGB image.
    """
    if not isinstance(filename, str):
        raise ValueError("filename should be a string.")
    if not os.path.isfile(filename):
        raise ValueError("Invalid file path.")
    raw_image = cv2.imread(filename, cv2.IMREAD_COLOR)
    if raw_image is None:
        raise ValueError("Failed to read image.")
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
    return image
