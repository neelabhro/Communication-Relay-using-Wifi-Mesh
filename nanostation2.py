#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import glob
import os
import subprocess

bridge = CvBridge()
img_dir = "/home/neelabhro/Desktop/comm_src/src/comm/src/send_folder"
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
count = 0
i = 0
loop = 0
length = len(files)
flag = 0
n = 0
m = 0
l = 0
flag1 = 0

path1 = "/home/neelabhro/Desktop/comm_src/src/comm/src/receive_folder"
os.chdir(path1)
a = subprocess.check_output("date")
subprocess.Popen(['mkdir', a])


def callback(msg):
	global i
	print("Receiving files from drone")
	try:
		cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
	except CvBridgeError, e:
		print(e)
	else:
		cv2.imwrite("/home/neelabhro/Desktop/comm_src/src/comm/src/receive_folder/" + str(a) + "/image" + str(a) + "%i.jpg"%i, cv2_img)
	i += 1
	
def sender():
	global length
	info_pub.publish(length)
	for f1 in files:
		print("sending file to drone")
		img = cv2.imread(f1)
		image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
		rate.sleep()
	flag = 1
	send_confirm.publish(flag)

def info(data):
	global n
	n = data.data
	print('No of files to be received: ', data.data)

def confirm(var):
	global m
	m += 1

def receive(var2):
	global l
	l += 1
	
	
def main():
	print('bbbbballlaaa')
	global count, loop, image_pub, info_pub, rate, flag, send_confirm, flag1, l
	rospy.init_node('nanostation1', anonymous = True)
	info_pub = rospy.Publisher('nano_info', Int32, queue_size = 10)
	rospy.Subscriber('drone_info', Int32, info)
	rospy.Subscriber('receive_topic', Int32, confirm)
	rospy.Subscriber('send_topic', Int32, receive)
	send_confirm = rospy.Publisher('confirmation', Int32, queue_size = 10)
	rospy.sleep(3)
	image_pub = rospy.Publisher('image_receiver_nano1', Image, queue_size = 10)
	rospy.Subscriber('image_sender', Image, callback)
	
	rate = rospy.Rate(1)
	
	while not (rospy.is_shutdown()):
		print('nnansnajsnjxan')
		inform = info_pub.get_num_connections()
		connections = image_pub.get_num_connections()

		if (inform == 1 and connections == 1 and flag1 == 0):
			print("drone connected")
			flag1 = 1

		if (i == n and l == 1):
			rospy.sleep(1)
			sender()
			print("all files sent")
			l = 0
		
		if (m == 1):
			print('all files received by drone')
			break
		rate.sleep()


	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
