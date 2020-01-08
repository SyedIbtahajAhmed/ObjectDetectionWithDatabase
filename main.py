import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error


# Convert digital data to binary format

def convertToBinaryData(filename):
    with open("C:\Python37\objectDetection\DetectedCars\dusricar0.jpg", 'rb') as file:
        binaryData = file.read()
    return binaryData

#Inserting picture

def insertBLOB(emp_id, Name, Photo):
    print("Inserting BLOB into detected cars")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='Car Detection project',
                                             user='root',
                                             password='')
        
                                        

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO detectedcars
                          (id, Name, Photo) VALUES (%s,%s,%s)"""

        #file = convertToBinaryData(biodataFile)
        empPicture = convertToBinaryData(Photo)

        # Convert data into tuple format
        insert_blob_tuple = (emp_id, Name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
cap = cv2.VideoCapture(0)
count=0
while True:
    _, frame = cap.read()

    height, width, channels = frame.shape


    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)


    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label == "car":
                ret,frame=cap.read()
                color = colors[i]
                a=cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
                b=cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                key=cv2.waitKey(1)
                if key==115:
                    car_det=cv2.imwrite("DetectedCars/dusricar%d.jpg" %count,frame)
                    car_detect=cv2.imread("DetectedCars/dusricar%d.jpg" %count)
                    cv2.imshow("Detected car",car_detect)
                    count +=1
                    cv2.waitKey(3000)
                    cv2.destroyWindow("Detected car")
                    insertBLOB(1, "Detected car:1", "C:\Python37\objectDetection\DetectedCars\dusricar0.jpg")
                    break
                
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

