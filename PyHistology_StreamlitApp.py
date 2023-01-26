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

import streamlit as st

import numpy as np
import cv2

from PIL import Image
from PIL import ImageColor

from skimage.color import rgb2gray

import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv

import os
import time
from io import BytesIO

import sys

# Don't generate the __pycache__ folder locally
sys.dont_write_bytecode = True 

# Print exception without the buit-in python warning
sys.tracebacklimit = 0 

########################################################################################

from scale_rgb_to_hsv import *

PAD = 15
FONTSIZE_TITLE = 18

########################################################################################

with open("logo.jpg", "rb") as f:
	image_data = f.read()

image_bytes = BytesIO(image_data)

st.set_page_config(page_title = 'PyDigitalHistology', page_icon = image_bytes, layout = "wide", initial_sidebar_state = "expanded", menu_items = {'Get help': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'Report a bug': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'About': 'This is a application for demonstrating the PyDigitalHistology package. Developed, tested and maintained by Ajinkya Kulkarni: https://github.com/ajinkya-kulkarni at the MPI-NAT, Goettingen'})

DPI = 500

# Title of the web app

st.title(':blue[Application for demonstrating the PyDigitalHistology package]')

st.markdown("")

########################################################################################

with st.form(key = 'form1', clear_on_submit = False):

	uploaded_file = st.file_uploader("Upload a 2D RGB histopathology image to be analyzed.", type=["tif", "tiff", "png", "jpg", "jpeg"], accept_multiple_files = False, label_visibility = 'visible')

	st.markdown("""---""")

	####################################################################################
	
	left_column1, middle_column1, right_column1  = st.columns(3)

	with left_column1:
		color = st.color_picker('Pick the lower color bound', '#00f900', label_visibility = "visible", key = '-LowerColorKey-')
		LowerColorKey = st.session_state['-LowerColorKey-']

		LowerColorHSV_scaled = scale_rgb_to_hsv(LowerColorKey)

	with middle_column1:
		color = st.color_picker('Pick the upper color bound', '#00f900', label_visibility = "visible", key = '-HigherColorKey-')
		HigherColorKey = st.session_state['-HigherColorKey-']

		HigherColorHSV_scaled = scale_rgb_to_hsv(HigherColorKey)

	with right_column1:
		st.slider('Threshold value', min_value = 100, max_value = 250, value = 180, step = 10, format = '%d', label_visibility = "visible", key = '-ThresholdValueKey-')
		ThresholdValueKey = int(st.session_state['-ThresholdValueKey-'])

	####################################################################################

	st.markdown("")

	submitted = st.form_submit_button('Analyze')

	st.markdown("")

	####################################################################################

	if uploaded_file is None:
		st.stop()

	if submitted:

		raw_image_from_pillow = Image.open(uploaded_file)

		raw_image = np.array(raw_image_from_pillow)

		HSV_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2HSV)

		################################################################################

		mask = cv2.inRange(HSV_image, LowerColorHSV_scaled, HigherColorHSV_scaled)

		output_HSV_image = cv2.bitwise_and(HSV_image, HSV_image, mask = mask)

		output_RGB_image = cv2.cvtColor(output_HSV_image, cv2.COLOR_HSV2RGB)

		################################################################################
		
		blue_pixels = np.count_nonzero(mask)
		
		################################################################################
		
		### Calcuate gray scale image
		
		image_gray = 255 * rgb2gray(raw_image)
					
		non_white_pixels = np.count_nonzero(image_gray < ThresholdValueKey)

		################################################################################

		percentage_area = np.round(100 * blue_pixels / non_white_pixels, 2)

		################################################################################

		mosaic = "AB"
		fig = plt.figure(figsize = (12, 6), constrained_layout = True, dpi = DPI)
		ax = fig.subplot_mosaic(mosaic)

		ax['A'].imshow(raw_image)
		ax['A'].set_title('Uploaded Image', pad = PAD, fontsize = FONTSIZE_TITLE)
		ax['A'].set_xticks([])
		ax['A'].set_yticks([])
		
		#####
		
		output_RGB_image_temp = output_RGB_image.copy()
		output_RGB_image_temp[np.all(output_RGB_image_temp == [0, 0, 0], axis = -1)] = [255, 255, 255]
		
		#####

		ax['B'].imshow(output_RGB_image_temp)
		ax['B'].set_title('Isolated pixels', pad = PAD, fontsize = FONTSIZE_TITLE)
		ax['B'].set_xticks([])
		ax['B'].set_yticks([])

		st.pyplot(fig)

		################################################################################

		st.stop()