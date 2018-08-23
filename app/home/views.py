from flask import Flask,abort,render_template,request,redirect,url_for,send_from_directory,flash,jsonify,json
from flask_login import current_user,login_required
from . import home
from ..models import User,ImageDB,SegmentedImage
from ..import db
from werkzeug import secure_filename
from forms import AddImageForm,EditImageForm
from os.path import join,dirname,realpath,abspath
import os 
from datetime import datetime
from functools import wraps
from urllib import urlencode, quote, unquote
import base64
import time
import pydicom
import subprocess
from PIL import Image,ImageFile

upload_folder="uploads/"
allowed_extensions=["jpg","png","jpeg","gif"]
jpg_global_name=""
dicom_global_name=""



def detect_multy(filename):
	ds=pydicom.dcmread(filename)
	number=0
	try:
		number=ds[0x28,0x08].value
	except Exception as e:
		number=1
	return number

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
	try:
		ds.data_element("Manufacturer").value=""
	except Exception as e:
		pass
	#try:
	#	ds.data_element("ImageType").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("SOPClassUID").value=""
	#except Exception as e:
	#	pass

	try:
		ds.data_element("StudyDate").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("SeriesDate").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("AcquisitionDate").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("ContentDate").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("StudyTime").value=""	
	except Exception as e:
		pass

	#try:
	#	ds.data_element("SOPInstanceUID").value=""
	#except Exception as e:
	#	pass

	try:
		ds.data_element("SeriesTime").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("AcquisitionTime").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("ContentTime").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("AccessionNumber").value=""
	except Exception as e:
		pass

	#try:
	#	ds.data_element("Modality").value=""
	#except Exception as e:
	#	pass

	try:
		ds.data_element("InstitutionName").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("ReferringPhysicianName").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("StationName").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("SeriesDescription").value=""
	except Exception as e:
		pass
	try:
		ds.data_element("InstitutionalDepartmentName").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("ManufacturerModelName").value=""
	except Exception as e:
		pass

	#try:
	#	ds.data_element("DerivationDescription").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("DerivationCodeSequence").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("ProtocolName").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("ScanOptions").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("RotationDirection").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("PatientPosition").value=""
	#except Exception as e:
	#	pass

	#try:
	#	ds.data_element("PatientOrientation").value=""
	#except Exception as e:
	#	pass
	#ds.data_element("LossyImageCompression").value=""
	#ds.data_element("LossyImageCompressionMethod").value=""
	#ds.data_element("PhotometricInterpretation").value=""
	try:
		ds.data_element("ImageComments").value=""
	except Exception as e:
		pass
	#ds.data_element("SliceThickness").value=""
	#ds.data_element("KVP").value=""
	try:
		ds.data_element("StudyID").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("SeriesNumber").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("AcquisitionNumber").value=""
	except Exception as e:
		pass

	try:
		ds.data_element("InstanceNumber").value=""
	except Exception as e:
		pass
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
	#for elem in ds.iterall():
	#	print(elem)
	#ds.BeamSequence=[Dataset(),Dataset(),Dataset()]
	#print(ds.BeamSequence[0])
	#print(ds.BeamSequence[0].Manufacturer)
	#print(ds.BeamSequence[1].Manufacturer)
	#print(ds.BeamSequence[2])
	ds.save_as(output_filename)
	

def allowed_file(filename):
	return "." in filename and \
		filename.rsplit(".",1) in allowed_extensions

@home.route("/admin/dashboard")
@login_required
def admin_dashboard():
	if not current_user.is_admin:
		abort(403)
	return render_template("home/admin_dashboard.html",title="Welcome to the Admin Page")

@home.route("/")
def homepage():
	return render_template("home/index.html",title="Welcome to the DICOM image")

@home.route("/dashboard")
@login_required
def dashboard():
	return render_template("home/dashboard.html",title="Welcome User!")

@home.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
	return send_from_directory(upload_folder+str(current_user.id),filename)

@home.route("/segmentation")
@login_required
def segmentation():
	#images=ImageDB.query.all()
	images=db.session.query(ImageDB).filter(ImageDB.user_id==current_user.id)
	return render_template("home/segmentations.html",images=images,title="Your Segmentation Images")

@home.route("/segmentedlist/<int:id>")
@login_required
def segmentedlist(id):
	images=db.session.query(SegmentedImage).filter(SegmentedImage.image_id==id)
	return render_template("home/segmentations2.html",images=images,parent_id=id,title="Your Segmentation Images")

@home.route("/test_dicom")
@login_required
def test_segmentation():
	return render_template("home/test_dicom.html",title="test dicom")

@home.route

@home.route("/editimage/<int:id>",methods=["GET","POST"])
@login_required
def edit_image(id):
	image=ImageDB.query.get_or_404(id)
	form=EditImageForm(obj=image)
	filename=image.image_filename
	original_path=os.getcwd()
	id_user=current_user.id
	image_path='app/uploads/'+str(id_user)
	if form.validate_on_submit():
		f_image=form.image_filename.data
		filename_image=secure_filename(f_image.filename)
		original_image_name=filename_image.split(".")[0]
		extensi_file=filename_image.split(".")[1]	
		#image=Image(image_name=form.image_name.data,image_description=form.image_description.data,image_filename=filename_image,user_id=current_user.id,image_date=datetime.now())		
		image.image_name=form.image_name.data
		image.image_description=form.image_description.data
		old_image_name=image.image_filename
		timestr=time.strftime("%Y%m%d-%H%M%S")
		last_filename=secure_filename(str(timestr)+"-"+original_image_name+"-"+str(id_user)+'.'+extensi_file)
			
		try:
			original_image_name
		except NameError:
			original_image_name=None	
		if original_image_name is not None:
			image.image_filename=last_filename
			os.chdir(image_path)
			os.remove(old_image_name)
			os.chdir(original_path)
			
		image.user_id=current_user.id
		image.image_date=datetime.now()
		db.session.commit()
		f_image.save(join(dirname(realpath(__file__)),
'..','uploads/'+str(id_user)+"/",last_filename))
		os.chdir(image_path)
		anonymize(last_filename,last_filename)
		number_of_frames=detect_multy(last_filename)
		image.image_frame_count=number_of_frames
		db.session.commit()
		os.chdir(original_path)
		flash("Image has been edited")
		return redirect(url_for("home.segmentation"))	
	return render_template("home/edit_segmentation.html",form=form,filename=filename,title="Edit Segmentation")



def confirmation_required(desc_fn):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.args.get('confirm') != '1':
                desc = desc_fn()
                return redirect(url_for('home.confirm', 
                    desc=desc, action_url=quote(request.url)))
            return f(*args, **kwargs)
        return wrapper
    return inner

@home.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = unquote(request.args['action_url'])

    return render_template('home/_confirm.html', desc=desc, action_url=action_url)

def you_sure():
    return "Are you sure?"

'''
@home.route('/')
@confirmation_required(you_sure)
def hello_world():
    return 'Hello World!'
'''

@home.route("/deleteimageajax2/<int:id>",methods=["GET","POST"])
@login_required
def delete_image_ajax2(id):
	"""
	Delete image from database
	"""
	segmented_image=SegmentedImage.query.get_or_404(id)
	id_image=segmented_image.id
	original_dir=os.getcwd()
	image_path='app/uploads/'+str(current_user.id)+'/'
	os.chdir(image_path)
	try:
		os.remove(segmented_image.image_filename)
		os.chdir(original_dir)
	except:
		os.chdir(original_dir)
	#db.session.query(SegmentedImage).filter(SegmentedImage.image_id==id_image).delete()
	db.session.delete(segmented_image)
	db.session.commit()
	#flash("You have successfully deleted the image")
	return json.dumps({'status':'OK'})	
	return render_template(title="Delete Image")


@home.route("/deleteimageajax/<int:id>",methods=["GET","POST"])
@login_required
def delete_image_ajax(id):
	"""
	Delete image from database
	"""
	image=ImageDB.query.get_or_404(id)
	id_image=image.id
	original_dir=os.getcwd()
	image_path='app/uploads/'+str(current_user.id)+'/'
	os.chdir(image_path)
	try:
		os.remove(image.image_filename)
		os.chdir(original_dir)
	except:
		os.chdir(original_dir)
	db.session.query(SegmentedImage).filter(SegmentedImage.image_id==id_image).delete()
	db.session.delete(image)
	db.session.commit()
	#flash("You have successfully deleted the image")
	return json.dumps({'status':'OK'})	
	return render_template(title="Delete Image")

@home.route("/deleteimage/<int:id>",methods=["GET","POST"])
@login_required
def delete_image(id):
	"""
	Delete image from database
	"""
	image=ImageDB.query.get_or_404(id)
	original_dir=os.getcwd()
	image_path='app/'+upload_folder
	os.chdir(image_path)
	os.remove(image.image_filename)
	os.chdir(original_dir)
	db.session.delete(image)
	db.session.commit()
	flash("You have successfully deleted the image")
	return redirect(url_for("home.segmentation"))	
	return render_template(title="Delete Image")


@home.route("/addimage",methods=["GET","POST"])
@login_required
def add_image():
	form=AddImageForm()
	if form.validate_on_submit():
		f_image=form.image_filename.data
		filename_image=secure_filename(f_image.filename)
		original_image_name=filename_image.split(".")[0]
		extensi_file=filename_image.split(".")[1]
		image=ImageDB(image_name=form.image_name.data,image_description=form.image_description.data,image_filename=filename_image,user_id=current_user.id,image_date=datetime.now())
		db.session.add(image)
		db.session.commit()

		user_id=image.user_id
		directory='app/uploads/'+str(user_id)+'/'
		timestr=time.strftime("%Y%m%d-%H%M%S")

		last_filename=secure_filename(str(timestr)+"-"+original_image_name+"-"+str(user_id)+'.'+extensi_file)

		try:
			os.stat(directory)
		except:
			os.mkdir(directory) 

		f_image.save(join(dirname(realpath(__file__)),'..','uploads/'+str(user_id)+'/',last_filename))
		original_path=os.getcwd()
		print(original_path)
		destination_path="app/uploads/"+str(user_id)+"/"
		os.chdir(destination_path)
		anonymize(last_filename,last_filename)
		number_of_frames=detect_multy(last_filename)
		image.image_frame_count=number_of_frames
		image.image_filename=last_filename
		os.chdir(original_path)
		db.session.commit()
		#path_image='uploads/'+current_user.id+'/'
		#os.mkdir(path_image,0777)
		#save original image
		#f_image.save(join(dirname(realpath(__file__)),'..',path_image,filename_image))
		
		#save png converted image


		#save jpg converted image

		flash("Image has been saved")
		
		return redirect(url_for('home.segmentation'))
	return render_template("home/add_segmentation.html",form=form,title="Adding Medical Image")


@home.route("/segmentimage/<int:id>",methods=["GET","POST"])
@login_required
def segment_image(id):
	parentid=id
	return render_template("home/painting2.html",parentid=id,title="Segment Medical Image")	

@home.route("/segmentimagesingle/<int:id>",methods=["GET","POST"])
@login_required
def segment_image_single(id):
	parentid=id
	return render_template("home/painting3.html",parentid=id,title="Segment Medical Image")


@home.route("/continuesegmentimagesingle/<int:id>",methods=["GET","POST"])
@login_required
def continue_segment_image_single(id):
	segmentedimage=SegmentedImage.query.get_or_404(id)
	parentid=segmentedimage.image_id
	return render_template("home/painting4.html",parentid=parentid,title="Segment Medical Image")

@home.route('/dist/<path:filename>')
def base_static(filename):
    #return os.getcwd()
    return send_from_directory('static/test_dicom/', filename)

def find_image(id):
	image=ImageDB.query.get_or_404(id)
	return image.image_filename


def find_segmented_image(id):
	image=SegmentedImage.query.get_or_404(id)
	return image.segmented_image_dicom_name

def find_segmented_image_comment(id):
	image=SegmentedImage.query.get_or_404(id)
	return image.segmented_image_comment

def find_frame_count(id):
	image=ImageDB.query.get_or_404(id)
	return image.image_frame_count

@home.route("/api/<int:id>",methods=["GET","POST"])
@login_required
def getapi(id):
	images_filename = find_image(id)
	return jsonify(file_name=images_filename,frame_images_count=find_frame_count(id))

@home.route("/apisegmented/<int:id>",methods=["GET","POST"])
@login_required
def getapisegmented(id):
	images_filename = find_segmented_image(id)
	segmented_image_comment=find_segmented_image_comment(id)
	return jsonify(file_name=images_filename,comment=segmented_image_comment)



@home.route("/view/<int:id>")
def view_image(id):
	return render_template("home/view_image.html",title="View Original Dataset")

@home.route("/viewsingle/<int:id>")
def view_image_single(id):
	return render_template("home/view_single_image.html",title="View Original Dataset")


@home.route("/viewsegmented/<int:id>")
def view_segmented_image(id):
	return render_template("home/view_segmented_image.html",title="View Segmented Image")

@home.route("/viewsegmentedsingle/<int:id>")
def view_segmented_image_single(id):
	return render_template("home/view_segmented_single_image.html",title="View Segmented Image")



def convert_and_save(b64_string):
	with open("imageToSave.png","wb") as fh:
		fh.write(base64.b64decode(b64_string.encode()))


@home.route("/confirmation",methods=["GET","POST"])
def confirmation():
	if request.method=="POST":
		d=request.form
		im_id=d["im_id"]
		confirm=d["confirm"]
		segmented_image_jpg_name=d["jpg_filename"]
		segmented_image_dicom_name=d["dicom_filename"]
		image_id=im_id
		segmented_image_comment=confirm
		segmented_images=SegmentedImage(segmented_image_jpg_name=segmented_image_jpg_name,segmented_image_dicom_name=segmented_image_dicom_name,image_id=image_id,segmented_image_comment=segmented_image_comment)
		db.session.add(segmented_images)
		db.session.commit()
		#for key,value in d.items():
		#	confirm=key
		#confirm=confirm.split(',',1)[-1]
		#some code to save confirmation box
		return "ok"
	else:
		return "error"

@home.route("/editconfirmation",methods=["GET","POST"])
def editconfirmation():
	if request.method=="POST":
		d=request.form
		im_id=d["im_id"]
		confirm=d["confirm"]
		segmented_image_jpg_name=d["jpg_filename"]
		segmented_image_dicom_name=d["dicom_filename"]
		image_id=im_id
		segmented_image_comment=confirm
		
		segmentedimage=SegmentedImage.query.get_or_404(im_id)
		segmentedimage.segmented_image_jpg_name=segmented_image_jpg_name
		segmentedimage.segmented_image_dicom_name=segmented_image_dicom_name
		segmentedimage.segmented_image_comment=segmented_image_comment
		db.session.commit()
		#segmented_images=SegmentedImage(segmented_image_jpg_name=segmented_image_jpg_name,segmented_image_dicom_name=segmented_image_dicom_name,image_id=image_id,segmented_image_comment=segmented_image_comment)
		#db.session.add(segmented_images)
		#db.session.commit()
		#for key,value in d.items():
		#	confirm=key
		#confirm=confirm.split(',',1)[-1]
		#some code to save confirmation box
		return "ok"
	else:
		return "error"

@home.route("/edit_uploaded_citra",methods=["GET","POST"])
def edit_uploaded_base64_file():
	if request.method=="POST":
		d=request.form
		for key,value in d.items():
			image=key
		image+='=='
		image=image.split(',',1)[-1]
		imageEncoded=base64.decodestring(image.encode())
		original_path=os.getcwd()
		id_user=current_user.id
		destination_path="app/uploads/"+str(id_user)+"/"
		os.chdir(destination_path)
		timestr=time.strftime("%Y%m%d-%H%M%S")
		image_filename="segmented-"+str(timestr)+".png"
		ImageFile.LOAD_TRUNCATED_IMAGES = True
		with open(image_filename,"wb") as fh:
			fh.write(imageEncoded)
			current_image=Image.open(image_filename)
			jpg_im=current_image.convert('RGB')
			jpg_image_filename="segmented-"+str(timestr)+".jpg"
			jpg_im.save(jpg_image_filename)
			dicom_image_filename="segmented-"+str(timestr)+".dcm"
			subprocess.call(["img2dcm",jpg_image_filename,dicom_image_filename])
			os.chdir(original_path)
			return jsonify(jpg_image_filename=jpg_image_filename,dicom_image_filename=dicom_image_filename)
	else:
		return "error"



@home.route('/save-record', methods=['POST'])
def save_record():
    app.logger.debug(request.files['file'].filename) 


@home.route("/upload_citra",methods=["GET","POST"])
def upload_base64_file():
	if request.method=="POST":
		d=request.form
		for key,value in d.items():
			image=key
		image+='=='
		image=image.split(',',1)[-1]
		imageEncoded=base64.decodestring(image.encode())
		original_path=os.getcwd()
		id_user=current_user.id
		destination_path="app/uploads/"+str(id_user)+"/"
		os.chdir(destination_path)
		timestr=time.strftime("%Y%m%d-%H%M%S")
		image_filename="segmented-"+str(timestr)+".png"
		ImageFile.LOAD_TRUNCATED_IMAGES = True

		with open(image_filename,"wb") as fh:
			fh.write(imageEncoded)
			current_image=Image.open(image_filename)
			jpg_im=current_image.convert('RGB')
			jpg_image_filename="segmented-"+str(timestr)+".jpg"
			#jpg_global_name=jpg_image_filename
			jpg_im.save(jpg_image_filename)
			dicom_image_filename="segmented-"+str(timestr)+".dcm"
			#dicom_global_name=dicom_image_filename
			subprocess.call(["img2dcm",jpg_image_filename,dicom_image_filename])
			'''
			current_image=Image.open(image_filename)
			jpg_im=current_image.convert("RGB")
			jpg_image_filename="segmented-"+str(timestr)+".jpg"
			dicom_image_filename="segmented-"+str(timestr)+".dcm"
			jpg_im.save(jpg_image_filename)
			subprocess.call(["img2dcm",jpg_image_filename,dicom_image_filename])
			'''
			os.chdir(original_path)
			return jsonify(jpg_image_filename=jpg_image_filename,dicom_image_filename=dicom_image_filename)
	else:
		return "error"
	'''
	if request.method == 'GET':
    	files = request.args.get('file')
        starter = files.find(',')
        image_data = files[starter+1:]
        image_data = bytes(image_data, encoding="ascii")
        with open('image.png', 'wb') as fh:
        	fh.write(base64.decodebytes(image_data))
       		return 'ok'
    return 'error'
	'''
	'''
	data=request.get_json()
	if data is None:
		print("data:"+data)
		print("No valid request body,json missing!")
		return jsonify({"error":"No valid request body,json missing!"})
	else:
		img_data=data["img"]
		convert_and_save(img_data)
	'''






