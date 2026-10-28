from pathlib import Path
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
with open("config.txt", "r") as f:
    bias_path = f.readline().strip()

bias_file = Path(bias_path)

bias_files = sorted(Path(bias_path).glob("bias_*.fit*"))

bias_stack = [fits.getdata(f) for f in bias_files]

bias_stack = np.array(bias_stack)

median=np.median(bias_stack, axis=0)

std=np.std(bias_stack, axis=0)

bad_pixels_mask = np.abs(bias_stack - median) > (3 * std)

masked_stack = np.ma.masked_array(bias_stack, mask=bad_pixels_mask)

master_bias_data = np.ma.median(masked_stack, axis=0).filled(median)

with fits.open(bias_files[0]) as hdul:
    header = hdul[0].header

header["COMBINED"] = True

hdu = fits.PrimaryHDU(data=master_bias_data, header=header)

hdu.writeto(Path(bias_path / "Master_Bias.fits"), overwrite=True)
#komentarz