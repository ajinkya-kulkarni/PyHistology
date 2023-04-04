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

import matplotlib.pyplot as plt

import time
from io import BytesIO

import sys
# Don't generate the __pycache__ folder locally
sys.dont_write_bytecode = True 
# Print exception without the buit-in python warning
sys.tracebacklimit = 0 

########################################################################################

from modules import *

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

st.set_page_config(page_title = 'PyHistology', page_icon = image_bytes, layout = "wide", initial_sidebar_state = "expanded", menu_items = {'Get help': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'Report a bug': 'mailto:ajinkya.kulkarni@mpinat.mpg.de', 'About': 'This is a application for demonstrating the PyHistology package. Developed, tested and maintained by Ajinkya Kulkarni: https://github.com/ajinkya-kulkarni at the MPI-NAT, Goettingen.'})

########################################################################################

# Title of the web app

st.title(':blue[Color space segmentation of H&E images]')

st.caption('For more information, have a look at this [screenshot](https://github.com/ajinkya-kulkarni/PyHistology/blob/main/StreamlitApp.jpg). Sample image to test this application is available [here](https://github.com/ajinkya-kulkarni/PyHistology/blob/main/TestImage.png). Source code available [here](https://github.com/ajinkya-kulkarni/PyHistology).', unsafe_allow_html = False)

st.markdown("")

########################################################################################

with st.form(key = 'form1', clear_on_submit = False):

	st.markdown(':blue[Upload a 2D RGB image to be analyzed.]')

	uploaded_file = st.file_uploader("Upload a file", type=["tif", "tiff", "png", "jpg", "jpeg"], accept_multiple_files = False, label_visibility = 'collapsed')

	####################################################################################
	
	st.markdown("""---""")

	####################################################################################

	st.markdown(':blue[Refer to the Hue and Saturation plot below to estimate the Hue and Saturation co-ordinates of the desired color to be extracted. Value goes from 0-255, 0 being the lowest brightness.]')

	st.markdown("")

	left_column1, right_column1  = st.columns(2)

	with left_column1:

		fig = plot_HSV_space('HSV_space.png', xnumber = XNUMBER, ynumber = YNUMBER, DPI = DPI, PAD = PAD, FONTSIZE_TITLE = FONTSIZE_TITLE, FIGSIZE = FIGSIZE)

		st.pyplot(fig)

	with right_column1:

		st.markdown("")

		st.slider('**Threshold value** in pixels, above which pixels are not evaluated.', min_value = 0, max_value = 255, value = 200, step = 5, format = '%d', label_visibility = "visible", key = '-ThresholdValueKey-')

		st.slider('**Hue** parameters for the lower & upper bound of the desired color.', min_value = 0, max_value = 180, value = [110, 130], step = 5, format = '%d', label_visibility = "visible", key = '-HueKey-')
		HueKey = st.session_state['-HueKey-']
		LowerHueKey = int(HueKey[0])
		HigherHueKey = int(HueKey[1])

		st.slider('**Saturation** parameters for the lower & upper bound of the desired color.', min_value = 0, max_value = 255, value = [10, 250], step = 5, format = '%d', label_visibility = "visible", key = '-SaturationKey-')
		SaturationKey = st.session_state['-SaturationKey-']
		LowerSaturationKey = int(SaturationKey[0])
		HigherSaturationKey = int(SaturationKey[1])

		st.slider('**Value** parameters for the lower & upper bound of the desired color.', min_value = 0, max_value = 255, value = [10, 250], step = 5, format = '%d', label_visibility = "visible", key = '-ValueKey-')
		ValueKey = st.session_state['-ValueKey-']
		LowerValueKey = int(ValueKey[0])
		HigherValueKey = int(ValueKey[1])

	####################################################################################

	st.markdown("")

	submitted = st.form_submit_button('Analyze')

	st.markdown("")
	
	####################################################################################

	if uploaded_file is None:
		st.stop()

	####################################################################################

	if submitted:

		ProgressBarText = st.empty()
		ProgressBarText.caption("Analyzing...")
		ProgressBar = st.progress(0)
		ProgressBarTime = 0.5

		ThresholdValueKey = int(st.session_state['-ThresholdValueKey-'])
		
		# Store the hue, saturation and brightness range selected by the user in numpy arrays LoweBoundNumbers and UpperBoundNumbers
		LowerBoundNumbers =  np.array([LowerHueKey, LowerSaturationKey, LowerValueKey])

		UpperBoundNumbers = np.array([HigherHueKey, HigherSaturationKey, HigherValueKey])

		time.sleep(ProgressBarTime)
		ProgressBar.progress(float(1/6))

		################################################################################

		try:
			
			# Access the file uploaded by the user 
			raw_image_from_pillow = Image.open(uploaded_file)
			
			# Make a numpy array composed of the 3-channels of RGB image 
			raw_image = np.array(raw_image_from_pillow)

			time.sleep(ProgressBarTime)
			ProgressBar.progress(float(2/6))
			
			#check if the image is a 3-channel image
			if raw_image.shape[-1] > 3:
				ErrorMessage = st.error('Image has more than 3 channels. Please upload an image with 3 channels', icon = None)
				time.sleep(SleepTime)
				ErrorMessage.empty()
				st.stop()
				
			# Convert the RGB image format to HSV format.
			HSV_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2HSV)

			time.sleep(ProgressBarTime)
			ProgressBar.progress(float(3/6))

			################################################################################
                        
			# Define a binary mask that stores only the pixels from the HSV image which are within the hue, saturation, and brightness range selected by the user.
			mask = cv2.inRange(HSV_image, LowerBoundNumbers, UpperBoundNumbers)

		    # Count all non-zero pixels in the mask
			pixels_of_interest = np.count_nonzero(mask)

			# Use bitwiseAND operator to multiply the mask with original HSV image.
            # New HSV image will contain pixels which were non-zero pixels in the mask. 
			output_HSV_image = cv2.bitwise_and(HSV_image, HSV_image, mask = mask)

			time.sleep(ProgressBarTime)
			ProgressBar.progress(float(4/6))
			
			# Convert the new HSV image back to RGB format.
			output_RGB_image = cv2.cvtColor(output_HSV_image, cv2.COLOR_HSV2RGB)

			time.sleep(ProgressBarTime)
			ProgressBar.progress(float(5/6))

			################################################################################

			### Convert the RGB image to grayscale 
			image_gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
                        
			# Count the number of pixels in the grayscale image that are above the threshold value.  
			non_white_pixels = np.count_nonzero(image_gray < ThresholdValueKey)

			################################################################################
			
			# Calculate the percentage of pixel of interest out of the total pixels in the image 
			percentage_area = np.round(100 * pixels_of_interest / non_white_pixels, 2)

			time.sleep(ProgressBarTime)
			ProgressBar.progress(float(6/6))

			time.sleep(ProgressBarTime)

			ProgressBarText.empty()
			ProgressBar.empty()

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
