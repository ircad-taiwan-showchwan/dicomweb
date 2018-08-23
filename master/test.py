import matplotlib.pyplot as plt
import pydicom
import os
from pydicom.data import get_testdata_files

print(os.getcwd())
print len(get_testdata_files('brain.dcm'))

ds=pydicom.dcmread("brain.dcm")
pydicom.dcmwrite("brain2.dcm",ds)
plt.imshow(ds.pixel_array,cmap=plt.cm.bone)
#filename=get_testdata_files('MRHead-8-slices.dcm')[0]

#ds=pydicom.dcmread(filename)

#plt.imshow(ds.pixel_array,cmap=plt.cm.bone)

