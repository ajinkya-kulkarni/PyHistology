[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pyhistology.streamlit.app/)
[![DOI](https://zenodo.org/badge/571896104.svg)](https://zenodo.org/badge/latestdoi/571896104)

# Color Space Segmentation using PyHistology

PyHistology is a package for color space segmentation of a user-uploaded 2D RGB image using the PyHistology package. It uses colorspace-based segmentation to analyze histopathology images. With the help of this package, you can easily calculate the amount of staining present in histopathology images. The application is also available as a Streamlit app and provides an interactive user interface with sliders, file uploaders, and progress bars.

### Prerequisites

- Python 3.7 or higher
- Streamlit library
- numpy
- cv2
- PIL
- skimage
- matplotlib

### Installation

1. Install Python 3.7 or higher
2. Install the required packages:

`pip install streamlit numpy opencv-python-headless pillow scikit-image matplotlib`

### App Overview

A web application developed using Streamlit is available at https://pyhistology.streamlit.app/

![alt text](https://github.com/ajinkya-kulkarni/PyHistology/blob/main/StreamlitApp.jpg)

### Usage
1. Clone the repository or download the source code
2. Navigate to the project directory and run the following command:
`streamlit run PyHistology_StreamlitApp.py`
3. The application will open in your default web browser. Upload a 2D RGB image to be analyzed and refer to the Hue and Saturation plot to estimate the Hue and Saturation co-ordinates of the desired color to be extracted. Use the sliders to adjust the threshold value, Hue, Saturation, and Value parameters for the lower and upper bound of the desired color. Click on the "Analyze" button to initiate the segmentation process.
4. The application will display the uploaded image, the HSV image, and the isolated pixels from the uploaded image. The isolated pixels are highlighted with a white color, and the percentage of the image area covered by the isolated pixels is displayed in the title of the output image.

### License
This application is licensed under the GNU Affero General Public License, Version 3. See the LICENSE file for more information.
