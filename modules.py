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

 # This file contains all the modules/functions necessary for running the streamlit application or the example notebooks.

########################################################################################

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

########################################################################################

def plot_HSV_space(image_path, xnumber, ynumber, DPI, PAD, FONTSIZE_TITLE, FIGSIZE):
	"""
	Plots the HSV color space using the given image.

	Parameters:
	image_path (str): The path to the image file.
	xnumber (int): The number of ticks on the x-axis.
	ynumber (int): The number of ticks on the y-axis.
	DPI (int): The DPI of the output image.
	PAD (int): The padding of the title.
	FONTSIZE_TITLE (int): The font size of the title.

	Returns:
	A figure object fig, which can be passed on later
	"""
	# Open the image using PIL and convert it to a numpy array
	HSV_space_image_raw = Image.open(image_path)
	HSV_space_image = np.array(HSV_space_image_raw)

	# Create the x-axis ticks and labels
	xticks_array = list(np.linspace(0, 2*255, xnumber))
	xlist_ticks = []
	for i in np.int_(xticks_array):
		xlist_ticks.append(str(int(i/2)))

	# Create the y-axis ticks and labels
	yticks_array = list(np.linspace(0, 2*180, ynumber))
	ylist_ticks = []
	for i in np.int_(yticks_array):
		ylist_ticks.append(str(int(i/2)))

	# Create the figure and plot the image
	fig = plt.figure(figsize=FIGSIZE, constrained_layout=True, dpi=DPI)
	plt.imshow(np.flipud(HSV_space_image), origin='lower')
	plt.xticks(xticks_array, xlist_ticks)
	plt.yticks(yticks_array, ylist_ticks)
	plt.xlabel('Saturation', fontsize = FONTSIZE_TITLE)
	plt.ylabel('Hue', fontsize = FONTSIZE_TITLE)
	plt.title('Hue and Saturation colorspace', pad = PAD, fontsize = FONTSIZE_TITLE)

	return fig

########################################################################################
