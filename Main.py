#!/usr/bin/env python
# coding: utf-8

# In[15]:


import cv2
import mediapipe as mp
import time
import pyautogui as pgi
from angle_calc import angle_calc
import os
import mimetypes
from tkinter import *  
from tkinter import messagebox  
from tkinter import filedialog

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

mimetypes.init()
root=Tk()
variable1=StringVar()    
variable2=StringVar()    

root.geometry("800x800")

l1 =Label(root, text = "Automated Posture assesment System", font= ('Helvetica 25 bold')).place(relx=.5, rely=0,anchor= N)
l2 =Label(root, textvariable = variable1, font= ('Helvetica 10 bold')).place(relx=.5, rely=.6,anchor= N)
l3 =Label(root, textvariable = variable2, font= ('Helvetica 10 bold')).place(relx=.5, rely=.7,anchor= N)


# In[16]:


import numpy as np

def calculate_angle(p1, p2, p3):
    # p1, p2, p3 are the points in format [x, y]
    # Calculate the vectors
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    # Calculate the angle in radians
    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    # Convert to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg
def image_pose_estimation(name):
    img = cv2.imread(name)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    pose1=[]
    joint_coord = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            x_y_z=[]
            h, w,c = img.shape
            x_y_z.append(lm.x)
            x_y_z.append(lm.y)
            x_y_z.append(lm.z)
            x_y_z.append(lm.visibility)
            pose1.append(x_y_z)
            cx, cy = int(lm.x*w), int(lm.y*h)
#             print([cx, cy])
            joint_coord.append([lm.x, lm.y])
            if id%2==0:
                cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
            else:
                cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)
    img = cv2.resize(img, (700, 700))
    cv2.imshow("Image", img)

#     print(joint_coord)
#     print(calculate_angle(joint_coord[11], joint_coord[13], joint_coord[15]))
    left_elbow = calculate_angle(joint_coord[11], joint_coord[13], joint_coord[15])

    right_elbow= calculate_angle(joint_coord[12], joint_coord[14], joint_coord[16])

    left_shoulder = calculate_angle(joint_coord[23], joint_coord[11], joint_coord[13])

    right_shoulder = calculate_angle(joint_coord[24], joint_coord[12], joint_coord[14])
    
    left_hip = calculate_angle(joint_coord[11], joint_coord[23], joint_coord[25])

    right_hip = calculate_angle(joint_coord[12], joint_coord[24], joint_coord[26])

    left_knee = calculate_angle(joint_coord[23], joint_coord[25], joint_coord[27])

    right_knee = calculate_angle(joint_coord[24], joint_coord[26], joint_coord[28])
    
    joint_angles = [left_elbow, right_elbow,left_shoulder,right_shoulder,left_hip,right_hip,left_knee,right_knee]
    rounded_list = [round(num, 2) for num in joint_angles]

# Print the rounded list
    print(rounded_list)
#     rula,reba=angle_calc(pose1)
#     print ([rula,reba])
#     if rula and reba:
#         if int(rula)>3:
#             pgi.alert("Posture not proper in upper body","Warning")
#         elif int(reba)>4:
#             pgi.alert("Posture not proper in your body","Warning")
#     variable1.set("Rapid Upper Limb Assessment Score : "+rula)
#     variable2.set("Rapid Entire Body Score : "+reba)
#     root.update()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

# def video_pose_estimation(name):
#     count=1
#     cap = cv2.VideoCapture(name)
#     while count:
#         frame_no=count*20
#         cap.set(1,frame_no);
#         success, img = cap.read()
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = pose.process(imgRGB)
#         pose1=[]
#         if results.pose_landmarks:
#             mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
#             for id, lm in enumerate(results.pose_landmarks.landmark):
#                 x_y_z=[]
#                 h, w,c = img.shape
#                 x_y_z.append(lm.x)
#                 x_y_z.append(lm.y)
#                 x_y_z.append(lm.z)
#                 x_y_z.append(lm.visibility)
#                 pose1.append(x_y_z)
#                 cx, cy = int(lm.x*w), int(lm.y*h)
#                 print([cx, cy])
#                 if id%2==0:
#                     cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
#                 else:
#                     cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)
#         img = cv2.resize(img, (600, 800))
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#         angle_calc(pose1)
#         time.sleep(1)
#         count+=1
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         exit()
#         rula,reba=angle_calc(pose1)
    
#         if (rula != "NULL") and (reba != "NULL"):
#             if int(rula)>3:
#                 variable1.set("Rapid Upper Limb Assessment Score : "+rula+"  Posture not proper in upper body")
#                 pgi.alert("Posture not proper in upper body","Warning")
#             else:
#                 variable1.set("Rapid Upper Limb Assessment Score : "+rula+"  Acceptable working posture")
#             if int(reba)>4:
#                 variable2.set("Rapid Entire Body Score : "+reba+"  Posture not proper in your body")
#                 pgi.alert("Posture not proper in your body","Warning")
#             else:
#                 variable2.set("Rapid Entire Body Score : "+reba+"   low risk")
#             root.update()
#         else:
#             pgi.alert("Posture Incorrect")

def webcam():
   video_pose_estimation(0)

def browsefunc():
   filename =filedialog.askopenfilename()
   mimestart = mimetypes.guess_type(str(filename))[0]

   if mimestart != None:
      mimestart = mimestart.split('/')[0]

   if mimestart == 'video':
      video_pose_estimation(str(filename))
   elif mimestart == 'image':
      image_pose_estimation(str(filename))
   else:
      pass
b1=Button(root,text="Browse for a video or an image",font=40,command=browsefunc).place(relx=.5, rely=.2,anchor= N)
b1=Button(root,text="Choose Live Posture Analysis using webcam",font=40,command=webcam).place(relx=.5, rely=.4,anchor= N)
root.mainloop()


# In[ ]:


joint_coord


# In[6]:


get_ipython().run_line_magic('pwd', '')


# In[6]:


print("R_Eye:",R_Eye,"L_Eye:",L_Eye)
print("R_Ear:",R_Ear,"L_Ear:",L_Ear)
print("R_Neck:",R_Neck,"L_Neck:",L_Neck)
print("R_Elbow:",R_Elbow,"L_Elbow:",L_Elbow)
print("R_Wrist:",R_Wrist,"L_Wrist:",L_Wrist)
print("R_Hip:",R_Hip,"L_Hip:",L_Hip)
print("R_Knee:",R_Knee,"L_Knee:",L_Knee)
print("R_Ankle:",R_Ankle,"L_Ankle:",L_Ankle)
print("R_Foot:",R_Foot,"L_Foot:",L_Foot)
print("R_Palm:",R_Palm,"L_Palm:",L_Palm)


# In[ ]:


a= [111.99, 165.14, 1.16, 17.1, 172.52, 170.72, 139.47, 179.89]
b= [176.17, 97.27, 53.28, 111.52, 140.83, 174.9, 132.84, 166.77]
c= [91.0, 72.12, 55.16, 34.25, 133.36, 175.44, 170.89, 165.59]
d= [178.06, 169.94, 55.88, 145.12, 91.68, 122.86, 118.59, 169.21]
e= [158.97, 22.66, 7.22, 120.75, 176.67, 136.94, 174.45, 163.1]
f= [167.81, 57.67, 27.33, 35.95, 174.52, 143.26, 167.49, 114.14]
g= [46.34, 21.73, 52.12, 52.12, 137.84, 130.69, 128.75, 168.22]
h= [154.08, 154.3, 106.68, 53.17, 109.84, 172.15, 100.88, 178.15]

