#! /usr/bin/python
# Copyright (c) 2015, Rethink Robotics, Inc.

# Using this CvBridge Tutorial for converting
# ROS images to OpenCV2 images
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

# Using this OpenCV2 tutorial for saving Images:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image,CompressedImage
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import time
import numpy as np
# Instantiate CvBridge
bridge = CvBridge()
img_name = "fuck.jpg"
img_file_path = "./"

def get_image_compressed():
        rospy.loginfo("Getting image...")
        image_msg = rospy.wait_for_message(
            "/usb_cam/image_raw/compressed",
            CompressedImage)
        rospy.loginfo("Got image!")

        # Image to numpy array
        np_arr = np.fromstring(image_msg.data, np.uint8)
        # Decode to cv2 image and store
        cv2_img = cv2.imdecode(np_arr,  cv2.IMREAD_COLOR)
        
        cv2.imwrite(img_file_path+"/"+img_name, cv2_img)
        rospy.loginfo("Saved to: " + img_file_path)
        return img_file_path

# def image_callback(msg):
#     print("Received an image!")
#     try:
#         # Convert your ROS Image message to OpenCV2
#         cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
#         rate = rospy.Rate(0.5)
#         rate.sleep()
#     except CvBridgeError, e:
#         print(e)
#     else:
#         # Save your OpenCV2 image as a jpeg 
#         cv2.imwrite(img_name, cv2_img)
        

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/usb_cam/image_raw"
    while not rospy.is_shutdown():
        get_image_compressed()
        rospy.sleep(1)

    # Set up your subscriber and define its callback
    # rospy.Subscriber(image_topic, Image, image_callback, queue_size=1)

    # Spin until ctrl + c
    # rospy.spin()

if __name__ == '__main__':
    main()