import face_recognition


def encoding_image():
	li_image = face_recognition.load_image_file('shen.jpg')
#	shen_image = face_recognition.load_image_file('shen.jpg')
	print('encoding known people')
	try:
		li_image_encoding = face_recognition.face_encodings(li_image)[0]
#		shen_image_encoding = face_recognition.face_encodings(shen_image)[0]
	except IndexError:
		print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
		quit()

	known_faces = [li_image_encoding]#,shen_image_encoding]
	return known_faces

def recognize_image(imageName,known_faces):
	print('recognizing image',imageName)
	unknown_image = face_recognition.load_image_file(imageName)
	try:
		unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
	except IndexError:
		print("Unable to locate any faces in at least one of the images. Check the image files. ")
		return False
	results = face_recognition.compare_faces(known_faces,unknown_face_encoding,0.5)
	if True in results:
		return True
	else:
		return False

print(recognize_image('16-29-18.jpg',known_faces=encoding_image()))
