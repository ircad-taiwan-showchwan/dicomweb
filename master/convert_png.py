import numpy as np
import png
import pydicom

path="brain.dcm"
ds=pydicom.dcmread(path)
shape=ds.pixel_array.shape

image_2d=ds.pixel_array.astype(float)
image_2d_scaled=(np.maximum(image_2d,0)/image_2d.max())*255.0

image_2d_scaled=np.uint8(image_2d_scaled)

with open("brainsz.png","wb") as png_file:
	w=png.Writer(shape[1],shape[0],greyscale=True)
	w.write(png_file,image_2d_scaled)
