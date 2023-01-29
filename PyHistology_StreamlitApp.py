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

import os
import time
from io import BytesIO

import sys

# Don't generate the __pycache__ folder locally
sys.dont_write_bytecode = True 

# Print exception without the buit-in python warning
sys.tracebacklimit = 0 

########################################################################################

from make_HSV_space_image import *

from extract_digits import *

########################################################################################

PAD = 12
FONTSIZE_TITLE = 12
DPI = 500

########################################################################################

with open("logo.jpg", "rb") as f:
	image_data = f.read()

image_bytes = BytesIO(image_data)

st.set_page_config(page_title = 'PyHistology', page_icon = image_bytes, layout = "wide", initial_sidebar_state = "expanded", menu_items = {'Get help': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'Report a bug': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'About': 'This is a application for demonstrating the PyHistology package. Developed, tested and maintained by Ajinkya Kulkarni: https://github.com/ajinkya-kulkarni at the MPI-NAT, Goettingen'})

########################################################################################

# Title of the web app

st.title(':blue[Application for demonstrating the PyHistology package]')

st.caption('For more information, visit https://github.com/ajinkya-kulkarni/PyHistology', unsafe_allow_html = False)

st.markdown("")

########################################################################################

with st.form(key = 'form1', clear_on_submit = False):

	uploaded_file = st.file_uploader("Upload a 2D RGB histopathology image to be analyzed.", type=["tif", "tiff", "png", "jpg", "jpeg"], accept_multiple_files = False, label_visibility = 'visible')

	st.markdown("""---""")

	####################################################################################

	left_column1, right_column1  = st.columns(2)

	with left_column1:

		plot_HSV_space('HSV_space.png', xnumber = 10, ynumber = 8, DPI = DPI, PAD = PAD, FONTSIZE_TITLE = FONTSIZE_TITLE)

	with right_column1:
		st.text_input('Hue, Saturation, Value values for the lower bound', value = '', placeholder = 'Example: 80, 20, 10', label_visibility = "visible", key = '-LowerBoundKey-')

		st.markdown("")

		st.text_input('Hue, Saturation, Value values for the upper bound', value = '', placeholder = 'Example: 120, 255, 255', label_visibility = "visible", key = '-UpperBoundKey-')

		st.markdown("")

		st.slider('Threshold value in pixels above which pixels are not evaluated', min_value = 50, max_value = 250, value = 200, step = 10, format = '%d', label_visibility = "visible", key = '-ThresholdValueKey-')

	st.markdown("""---""")

	####################################################################################

	st.markdown("")

	submitted = st.form_submit_button('Analyze')

	st.markdown("")

	####################################################################################

	if uploaded_file is None:
		st.stop()

	if submitted:

		ThresholdValueKey = int(st.session_state['-ThresholdValueKey-'])

		LowerBoundKey = list(st.session_state['-LowerBoundKey-'])
		LowerBoundNumbers =  np.int_(extract_consecutive_digits(LowerBoundKey))
		if (str(LowerBoundKey) == ""):
			ErrorMessage = st.error('Lower bound should not be empty', icon = None)
			time.sleep(SleepTime)
			ErrorMessage.empty()
			st.stop()

		UpperBoundKey = list(st.session_state['-UpperBoundKey-'])
		UpperBoundNumbers =  np.int_(extract_consecutive_digits(UpperBoundKey))
		if (str(UpperBoundKey) == ""):
			ErrorMessage = st.error('Upper bound should not be empty', icon = None)
			time.sleep(SleepTime)
			ErrorMessage.empty()
			st.stop()

		################################################################################

		raw_image_from_pillow = Image.open(uploaded_file)

		raw_image = np.array(raw_image_from_pillow)

		HSV_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2HSV)

		################################################################################

		mask = cv2.inRange(HSV_image, LowerBoundNumbers, UpperBoundNumbers)

		pixels_of_interest = np.count_nonzero(mask)

		output_HSV_image = cv2.bitwise_and(HSV_image, HSV_image, mask = mask)

		output_RGB_image = cv2.cvtColor(output_HSV_image, cv2.COLOR_HSV2RGB)

		################################################################################
		
		### Calcuate gray scale image

		image_gray = 255 * rgb2gray(raw_image)

		non_white_pixels = np.count_nonzero(image_gray < ThresholdValueKey)

		################################################################################

		percentage_area = np.round(100 * pixels_of_interest / non_white_pixels, 2)

		################################################################################

		mosaic = "AB"
		fig = plt.figure(figsize = (14, 10), constrained_layout = True, dpi = DPI)
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
		ax['B'].set_title('Isolated pixels, ' + str(percentage_area) + '%', pad = PAD, fontsize = FONTSIZE_TITLE)
		ax['B'].set_xticks([])
		ax['B'].set_yticks([])

		st.pyplot(fig)

		################################################################################

		st.stop()