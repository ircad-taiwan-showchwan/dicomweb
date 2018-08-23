import os,os.path
import pydicom

def anonymize(filename,output_filename,new_person_name="anonymus",new_patient_id="id",remove_curves=True,remove_private_tags=True):
	def PN_callback(ds,data_element):
		if data_element.VR=="PN":
			data_element.value=new_person_name
	
	def curves_callback(ds,data_element):
		if data_element.tag.group & 0xFF00==0x5000:
			del ds[data_element.tag]
	
	ds=pydicom.dcmread(filename)
	#print(ds.PatientName)
	#print(ds.PatientID)
	ds.walk(PN_callback)	
	ds.PatientID=new_patient_id
	for name in ["OtherPatientIDs","OtherPatientIDsSequence"]:
		if name in ds:
			delattr(ds,name)
	for name in ["PatientBirthDate"]:
		if name in ds:
			ds.data_element(name).value=""
	if remove_private_tags:
		ds.remove_private_tags()
	if remove_curves:
		ds.walk(curves_callback)
	'''	
	ds.data_element("Manufacturer").value=""
	ds.data_element("ImageType").value=""
	ds.data_element("SOPClassUID").value=""
	ds.data_element("StudyDate").value=""
	ds.data_element("SeriesDate").value=""
	#ds.data_element("AcquisitionDate").value=""
	#ds.data_element("ContentDate").value=""
	#ds.data_element("StudyTime").value=""	
	#ds.data_element("SOPInstanceUID").value=""
	#ds.data_element("SeriesTime").value=""
	#ds.data_element("AcquisitionTime").value=""
	#ds.data_element("ContentTime").value=""
	ds.data_element("AccessionNumber").value=""
	ds.data_element("Modality").value=""
	ds.data_element("InstitutionName").value=""
	ds.data_element("ReferringPhysicianName").value=""
	ds.data_element("StationName").value=""
	ds.data_element("SeriesDescription").value=""
	ds.data_element("InstitutionalDepartmentName").value=""
	ds.data_element("ManufacturerModelName").value=""
	ds.data_element("DerivationDescription").value=""
	ds.data_element("DerivationCodeSequence").value=""
	ds.data_element("ProtocolName").value=""
	ds.data_element("ScanOptions").value=""
	ds.data_element("RotationDirection").value=""
	ds.data_element("PatientPosition").value=""
	ds.data_element("PatientOrientation").value=""
	#ds.data_element("LossyImageCompression").value=""
	#ds.data_element("LossyImageCompressionMethod").value=""
	#ds.data_element("PhotometricInterpretation").value=""
	ds.data_element("ImageComments").value=""
	#ds.data_element("SliceThickness").value=""
	#ds.data_element("KVP").value=""
	ds.data_element("StudyID").value=""
	ds.data_element("SeriesNumber").value=""
	#ds.data_element("AcquisitionNumber").value=""
	#ds.data_element("InstanceNumber").value=""
	
	#ds.data_element("ImagePosition").value=""
	#ds.data_element("ImageOrientation").value=""
	#ds.data_element("FrameOfReferenceUID").value=""
	#ds.data_element("FrameOfReferenceIndicator").value=""
	#ds.data_element("RequestedProcedureID").value=""
	#ds.data_element("SoftwareVersion").value=""
	#ds.data_element("CodeValue").value=""
	#ds.data_element("CodingSchemeDesignator").value=""
	#ds.data_element("CodeMeaning").value=""
	#ds.data_element("PatientSex").value=""
	#ds.data_element("ScanOptions").value=""
	#ds.data_element("SliceThickness").value=""
	#ds.data_element("KVP").value=""
	'''
	#print(ds.data_element("NumberOfFrames"))
	#for elem in ds.iterall():
	#	print(elem)
	#ds.BeamSequence=[Dataset(),Dataset(),Dataset()]
	#print(ds.BeamSequence[0])
	#print(ds.BeamSequence[0].Manufacturer)
	#print(ds.BeamSequence[1].Manufacturer)
	#print(ds.BeamSequence[2])
	#ds.save_as(output_filename)
	
def detect_multy(filename):
	ds=pydicom.dcmread(filename)
	number=0
	#print(ds[0x28,0x08].value)
	try:
		number=ds[0x28,0x08].value
	#finally:
	except Exception as e:
		number=1
	return number
	#print(number)
	'''
	try:
		#number=ds.data_element("NumberOfFrame").value
		number=ds[0x28,0x08].value
		number=ds.NumberOfFrame
	except:
		number=1
	return number
	'''
if __name__=="__main__":
	img="20180730-201830-IM-0001-0563-7.dcm"
	#img="tes.dcm"
	#img="multi.dcm"
	anonymize(img,"tes.dcm")
	print(detect_multy(img))
