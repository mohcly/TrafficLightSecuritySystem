# TrafficLightSecuritySystem

This code implements a Traffic Light Security System using a Raspberry Pi board, an ESP32-CAM, and OpenCV. The system is designed to detect when a driver misses a traffic light and sends an email notification with an attached image of the car's license plate to the car's owner.

# Requirements

* Python 3.7+
* OpenCV
* pyFirmata
* smtplib

# Code Overview

* Import required libraries
* Configure email credentials and Arduino board
* Define pin number constants and necessary functions
* Set up the camera and initialize CascadeClassifier with the license plate haarcascade xml file
* Continuously loop and detect traffic light misses by reading the analog pin connected to a PIR sensor
* Send an email notification with an attached image of the car's license plate if the driver misses the traffic light more than two times
* Optionally, save the license plate image locally on the Raspberry Pi for future reference

The code makes use of OpenCV to detect license plates in the images captured by the ESP32-CAM. The cascade classifier is trained using haarcascade_russian_plate_number.xml. If the area of the detected license plate exceeds a certain minimum area, a rectangle is drawn around it. The ESP32-CAM takes the image and sends it to the Raspberry Pi through the HTTP protocol. The PIR sensor connected to an analog pin of the Arduino board is used to detect motion in front of the traffic light. If the driver misses the traffic light, an email notification is sent to the car's owner with the attached image of the car's license plate. The system keeps track of the number of times the driver misses the traffic light and sends the email notification only if it happens more than two times.

# Running the code

* Connect the ESP32-CAM to your Wi-Fi network.
* Ensure that the PIR sensor is connected to the analog pin of your Arduino board.
* Configure the email credentials in the code.
* Run the code.
