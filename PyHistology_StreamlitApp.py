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

# UX/UI recommendations provided by Radhika Bhagwat (radhika.bhagwat3@gmail.com, Product Designer)

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

from make_HSV_colorspace_image import *

########################################################################################

SleepTime = 2

FONTSIZE_TITLE = 10
PAD =FONTSIZE_TITLE
DPI = 500
FIGSIZE = (5, 5)

XNUMBER, YNUMBER = 10, 10

########################################################################################

with open("logo.jpg", "rb") as f:
	image_data = f.read()

image_bytes = BytesIO(image_data)

st.set_page_config(page_title = 'PyHistology', page_icon = image_bytes, layout = "wide", initial_sidebar_state = "expanded", menu_items = {'Get help': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'Report a bug': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'About': 'This is a application for demonstrating the PyHistology package. Developed, tested and maintained by Ajinkya Kulkarni: https://github.com/ajinkya-kulkarni at the MPI-NAT, Goettingen'})

########################################################################################

# Title of the web app

st.title(':blue[Color space segmentation using PyHistology]')

st.caption('For more information or to give feedback, visit https://github.com/ajinkya-kulkarni/PyHistology.', unsafe_allow_html = False)

st.markdown("")

########################################################################################

with st.form(key = 'form1', clear_on_submit = False):

	st.markdown(':blue[Upload a 2D RGB image to be analyzed.]')

	uploaded_file = st.file_uploader("Upload a file", type=["tif", "tiff", "png", "jpg", "jpeg"], accept_multiple_files = False, label_visibility = 'collapsed')

	####################################################################################
	
	st.markdown("""---""")

	st.markdown(':blue[Threshold value in pixels, above which pixels are not evaluated.]')

	st.slider('Threshold value in pixels, above which pixels are not evaluated.', min_value = 0, max_value = 255, value = 200, step = 5, format = '%d', label_visibility = "collapsed", key = '-ThresholdValueKey-')

	####################################################################################

	st.markdown("""---""")

	st.markdown(':blue[Refer to the Hue and Saturation plot below to estimate the Hue and Saturation co-ordinates of the desired color to be extracted. Value goes from 0-255, 0 being the lowest brightness.]')

	st.markdown("")

	left_column1, middle_column1, right_column1  = st.columns(3)

	with left_column1:

		plot_HSV_space('HSV_space.png', xnumber = XNUMBER, ynumber = YNUMBER, DPI = DPI, PAD = PAD, FONTSIZE_TITLE = FONTSIZE_TITLE, FIGSIZE = FIGSIZE)

	with middle_column1:

		st.slider('Hue parameter for the **lower bound** of the desired color.', min_value = 0, max_value = 180, value = 110, step = 1, format = '%d', label_visibility = "visible", key = '-LowerHueKey-')
		LowerHueKey = int(st.session_state['-LowerHueKey-'])

		st.slider('Saturation parameter for the **lower bound** of the desired color.', min_value = 0, max_value = 255, value = 10, step = 1, format = '%d', label_visibility = "visible", key = '-LowerSaturationKey-')
		LowerSaturationKey = int(st.session_state['-LowerSaturationKey-'])

		st.slider('Value parameter for the **lower bound** of the desired color.', min_value = 0, max_value = 255, value = 10, step = 1, format = '%d', label_visibility = "visible", key = '-LowerValueKey-')
		LowerValueKey = int(st.session_state['-LowerValueKey-'])

	with right_column1:

		st.slider('Hue parameter for the **higher bound** of the desired color.', min_value = 0, max_value = 180, value = 130, step = 1, format = '%d', label_visibility = "visible", key = '-HigherHueKey-')
		HigherHueKey = int(st.session_state['-HigherHueKey-'])

		st.slider('Saturation parameter for the **higher bound** of the desired color.', min_value = 0, max_value = 255, value = 255, step = 1, format = '%d', label_visibility = "visible", key = '-HigherSaturationKey-')
		HigherSaturationKey = int(st.session_state['-HigherSaturationKey-'])

		st.slider('Value parameter for the **higher bound** of the desired color.', min_value = 0, max_value = 255, value = 255, step = 1, format = '%d', label_visibility = "visible", key = '-HigherValueKey-')
		HigherValueKey = int(st.session_state['-HigherValueKey-'])

	####################################################################################

	st.markdown("")

	submitted = st.form_submit_button('Analyze')
	
	####################################################################################

	if uploaded_file is None:
		st.stop()

	if submitted:

		ThresholdValueKey = int(st.session_state['-ThresholdValueKey-'])

		LowerBoundNumbers =  np.array([LowerHueKey, LowerSaturationKey, LowerValueKey])

		UpperBoundNumbers = np.array([HigherHueKey, HigherSaturationKey, HigherValueKey])

		################################################################################

		try:

			raw_image_from_pillow = Image.open(uploaded_file)

			raw_image = np.array(raw_image_from_pillow)

			if raw_image.shape[-1] > 3:
				ErrorMessage = st.error('Image has more than 3 channels. Please upload an image with 3 channels', icon = None)
				time.sleep(SleepTime)
				ErrorMessage.empty()
				st.stop()

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

		except:

			ErrorMessage = st.error('Error with analyzing the image', icon = None)
			time.sleep(SleepTime)
			ErrorMessage.empty()
			st.stop()

		################################################################################

		left_column2, middle_column1, right_column2  = st.columns(3)

		with left_column2:

			fig = plt.figure(figsize = FIGSIZE, constrained_layout = True, dpi = DPI)

			plt.imshow(raw_image)
			plt.title('Uploaded Image', pad = PAD, fontsize = FONTSIZE_TITLE)
			plt.xticks([])
			plt.yticks([])

			st.pyplot(fig)

		#####

		with middle_column1:

			fig = plt.figure(figsize = FIGSIZE, constrained_layout = True, dpi = DPI)

			plt.imshow(HSV_image)
			plt.title('HSV Image', pad = PAD, fontsize = FONTSIZE_TITLE)
			plt.xticks([])
			plt.yticks([])

			st.pyplot(fig)

			#####

		with right_column2:

			output_RGB_image_temp = output_RGB_image.copy()
			output_RGB_image_temp[np.all(output_RGB_image_temp == [0, 0, 0], axis = -1)] = [255, 255, 255]

			plt.imshow(output_RGB_image_temp)
			plt.title('Isolated pixels from uploaded image, ' + str(percentage_area) + '%', pad = PAD, fontsize = FONTSIZE_TITLE)
			plt.xticks([])
			plt.yticks([])

			st.pyplot(fig)

		################################################################################

		st.stop()
