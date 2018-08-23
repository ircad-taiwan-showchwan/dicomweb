import matplotlib.pyplot as plt
import pydicom

from pydicom.data import get_testdata_files
#filename=get_testdata_files("MRHead-8-slices.dcm")[0]
#print(filename)
#ds=pydicom.dcmread("MRHead-8-slices.dcm")
ds=pydicom.dcmread("brain.dcm")
plt.imshow(ds.pixel_array,cmap=plt.cm.bone)
#for elem in ds:
#	print elem
#plt.imshow(ds.pixel_array,cmap=plt.cm.bone)

