#!/usr/bin/env python
# coding: utf-8

# In[1]:


import face_recognition, os, cv2, time
from PIL import Image,ImageDraw
import tensorflow as tf
import numpy as np

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

        print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

#helper functions
def generate_people_boxes(frame):
    #get the bounding boxes of humans
    boxes, scores, classes, num = odapi.processFrame(frame)
    people_box = []  #people_box stores a list of the coordinates of the person in the image

    for i in range(len(boxes)):
        # Class 1 represents human
        if classes[i] == 1 and scores[i] > threshold:
            people_box.append(boxes[i])
    return people_box

def crop_img(image,box):
    #returns an image object
    return image[box[0]:box[2], box[1]:box[3]]

def draw_box(image,box):
    #draw a box on the original image
    cv2.rectangle(image,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)        

def create_encoding(img_path):
    face_image = face_recognition.load_image_file(img_path)
    return face_recognition.face_encodings(face_image)[0]

def resize_aspect_ratio(img):
    #resize to fit the width requirements without changing aspect ratio
    height, width , channels = img.shape
    scale_factor = 400/height
    return cv2.resize(img, (int(scale_factor*width), int(scale_factor*height)))
    
    
def face_recognize(human_image):
    human_image = resize_aspect_ratio(human_image)
    
    resized_height , resized_width, _= human_image.shape

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_human_image = human_image[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_human_image)
    face_encodings = face_recognition.face_encodings(rgb_human_image, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.4)
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)
    return face_locations , face_names, resized_height, resized_width

def show_image(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def img_location_cal(crop_img_box,face_location_crop,resized_height,resized_width):
    #because we rescaled the images we need to now resize them back to original image
    crop_img_height = crop_img_box[2]- crop_img_box[0]
    crop_img_width = crop_img_box[3]- crop_img_box[1]
    top_left_y = crop_img_box[0]+ int(face_location_crop[0]/resized_height*crop_img_height)
    top_left_x = crop_img_box[1]+ int(face_location_crop[3]/resized_width*crop_img_width)
    btm_right_y = crop_img_box[0]+ int(face_location_crop[2]/resized_height*crop_img_height)
    btm_right_x = crop_img_box[1]+ int(face_location_crop[1]/resized_width* crop_img_width)
    return [top_left_y,top_left_x,btm_right_y,btm_right_x]


# In[39]:


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic  tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.


#import details of the model
root_path = os.getcwd()
model_path = root_path + '/mobilenet/frozen_inference_graph.pb'
odapi = DetectorAPI(path_to_ckpt=model_path)
threshold = 0.7
video_capture = cv2.VideoCapture(0)
human_database = {'Unknown':{'crime':'No Crime', 'probability':1}}
known_face_names=[]
known_face_encodings=[]

#load the criminals.txt file and do the encodings for all the individuals
with open(root_path+'/database/criminals.txt','r') as csv_file:
    for line in csv_file:
        entry= line.split(',')
        entry[-1] = entry[-1].strip()
        human_database[entry[0]] = {'crime':entry[1],'probability':entry[2]}
        
for key,value in human_database.items():
    if key!= 'Unknown':
        known_face_names.append(key)
        known_face_encodings.append(create_encoding(root_path+'/database/'+ '{0}.jpg'.format(key)))


# In[40]:


process_this_frame = True
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    frame = cv2.resize(frame,(1280,720))
    frame = cv2.flip(frame,1)

    if process_this_frame:
        #get the bounding boxes of humans
        people_box = generate_people_boxes(frame)
        face_pos_dic = {}

        #generate all the bounding boxes and names and save them in a dictionary
        for box in people_box:
            cropped_img = crop_img(frame, box)
            face_locations_onecrop , face_names_onecrop, resized_height, resized_width = face_recognize(cropped_img)
            for i in range(len(face_names_onecrop)):
                if face_names_onecrop[i] not in face_pos_dic:
                    face_pos_dic[face_names_onecrop[i]] = img_location_cal(box, face_locations_onecrop[i] ,resized_height,resized_width)
    
    process_this_frame = not process_this_frame

    #draw the bounding boxes on the original figure
    for (key,value) in face_pos_dic.items():
        left = value[1]
        top = value[0]
        right = value[3]
        bottom = value[2]
        
        if human_database[key]['crime'] == "No Crime":
            color = (0,255,0)
            textcolor = (255,255,255)

        elif human_database[key]['crime'] == "High":
            color = (0,0,255)
            textcolor = (255,255,255)

        else:
            color = (0,255,230)
            textcolor = (0,0,0)
        
        cv2.rectangle(frame, (left,top), (right,bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, key + ' '+ human_database[key]['crime']+ " crime", (left + 6, bottom - 6), font, 0.7, textcolor, 1)
   
    cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

