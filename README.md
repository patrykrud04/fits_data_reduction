# fits_data_reduction

Python scripts for reducing and visualizing astronomical observational data in the `.fits` format.

#  What's inside
* **Master Frame Creation & Plotting (`functions.py`):** Combines raw `.fits` files into master calibration frames and visualizes them. Built with modular functions, allowing you to generate master frames independently without plotting.


## Usage

1. Create a `path.txt` file containing the paths to the folders with your raw `.fits` files.
2. Call the functions to stack the frames and save the resulting master `.fits` file (plotting the histogram is optional).
