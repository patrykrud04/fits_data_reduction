from pathlib import Path
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


def get_path(line_number, config_file="paths.txt"):
    with open(config_file, "r") as f:
        lines = f.readlines()
    if len(lines) >= line_number:
        path_str = lines[line_number - 1].strip()
        return Path(path_str)
    else:
        raise IndexError(f"File has less than {line_number} lines")


def create_data_stack(directory_path, file_pattern):
    files = sorted(directory_path.glob(file_pattern))
    if not files:
        raise FileNotFoundError(f"No files found for pattern {file_pattern} in {directory_path}")
    stack = [fits.getdata(f) for f in files]
    header = fits.getheader(files[0])
    return np.array(stack), header


def create_master(data_stack, sigma=3):
    median = np.median(data_stack, axis=0)
    std = np.std(data_stack, axis=0)
    bad_pixels_mask = np.abs(data_stack - median) > (sigma * std)
    masked_stack = np.ma.masked_array(data_stack, mask=bad_pixels_mask)
    master_data = np.ma.median(masked_stack, axis=0).filled(median)
    return master_data


def save_master(directory_path, output_name, master_data, header):
    header["COMBINED"] = True
    hdu = fits.PrimaryHDU(data=master_data, header=header)
    output_path = directory_path / output_name
    hdu.writeto(output_path, overwrite=True)


def plot_histogram(data, title="FITS Data Histogram", bins=256):
    plt.figure(figsize=(10, 4))
    bins = np.linspace(0,1500,60)
    plt.hist(data.ravel(),bins=bins,label="data")
    plt.yscale('log')
    plt.title(title)
    plt.xlabel("ADU Value")
    plt.ylabel("Pixel Count")
    plt.grid(True)
    plt.show()