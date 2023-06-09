from firebase import firebase
import threading
import time
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'tivastorage'
bucket = storage_client.create_bucket(bucket_name)
print('Bucket {} created.'.format(bucket.name))

firebase = firebase.FirebaseApplication("https://microcontroller-tivac.firebaseio.com/", None)
cap = cv2.VideoCapture(0)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def WaitnChangeS():
    time.sleep(5)
    firebase.put('/Camera/-LuiexdwEVyLnDL1py-V', 'State', False)

def WaitnChangeA():
    time.sleep(30)
    firebase.put('/Camera/-LuiexdwEVyLnDL1py-V', 'Alert', False)

def Checkforimg():
    if firebase.get('/Camera/-LuiexdwEVyLnDL1py-V/Doorbell', ''):
        firebase.put("/Camera/-LuiexdwEVyLnDL1py-V", "img", cap.read())
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    mountainsRef = storageRef.child(frame)
    #t5 = threading.Thread(target=Checkforimg, args=())
    #t5.start()
    for obj in decodedObjects:
        print(obj.data)
        if str(obj.data) == "b'Open_The_Door'":
            t1 = threading.Thread(target=firebase.put, args=('/Camera/-LuiexdwEVyLnDL1py-V', 'State', True))
            t1.start()
            t3 = threading.Thread(target=WaitnChangeS, args=())
            t3.start()
        elif str(obj.data) != "b'Open_The_Door'":
            t2 = threading.Thread(target=firebase.put, args=('/Camera/-LuiexdwEVyLnDL1py-V', 'Alert', True))
            t2.start()
            t4 = threading.Thread(target=WaitnChangeA, args=())
            t4.start()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
