import cv2
import time
import urllib.request
import smtplib
import imghdr
import pyfirmata
from pyfirmata import Arduino
from email.message import EmailMessage
from time import sleep
import numpy as np

#Email Configuration
email_address = 'tlls.test.project@gmail.com'
email_password = 'migCac-2wuvfy-nohpor'
miss_count = 0
shots_count = 0
count = 0

#Arduino Configuration
port = "/dev/cu.usbmodem101"
board = Arduino(port)
sleep(.5)

green = 2
red = 3

def OnOnly(pin):
    board.digital[pin].write(1)
def OffOnly(pin):
    board.digital[pin].write(0)


# def blinkedLED(pin, msg):
#     print(msg)
#     board.digital[pin].write(1)
#     sleep(0.5)
#     board.digital[pin].write(0)
#     sleep(.5)
def sendWarning(title, msg_content, images, email):
    msg = EmailMessage()
    msg['Subject'] = title
    msg['from'] = email_address
    msg['To'] = email
    msg.set_content(msg_content)
    if images[0] == images[1]:
        pass
    else:
        for images in images:
            with open(images, 'rb') as file:
                file_data = file.read()
                file_type = imghdr.what(file.name)
                file_name = file.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

it = pyfirmata.util.Iterator(board)
it.start()

pirPin = board.get_pin("a:3:i")
# ledPin = 13

#ESP332_cam Configurations
url = 'http://172.20.10.12/cam-mid.jpg'
# img_cam = cv2.VideoCapture(0)
##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
plateCascade = cv2.CascadeClassifier('ressources/haarcascade_russian_plate_number.xml')
minArea = 500


while True:
    # turnOn(green, 1)
    # turnOn(yellow, 1)
    timeout = 25 # [seconds]
    timeStop_green = 15
    timeout_start = time.time()

    while time.time() < timeout_start + timeout:
        if time.time() < timeout_start + timeStop_green:
            OnOnly(green)
            OffOnly(red)
        elif time.time() < timeout_start + timeout:
            OnOnly(red)
        else:
            pass
        print(count)
        count += 1

        # OffOnly(red)
        # normalOn(red, 0.5)
        # success, img = img_cam.read()
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        numberPlate = plateCascade.detectMultiScale(gray, 1.15, 4)

        # Drawing rectangle around the number plate
        for (x, y, w, h) in numberPlate:
            area = w * h
            if area > minArea:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 4)

                croppedPlate = img[y:y + h, x:x + w]
                cv2.imshow("Cropped Number Plate", croppedPlate)

        if time.time() > timeout_start+timeStop_green:
            value = pirPin.read()
            print(value)
            # sleep(0.0001)
        else:
            value = None
        if value is None:
            pass
        elif float(value) > 0.6:
            miss_count += 1;
            # blinkedLED(ledPin, "Motion Detected")
            # sleep(.00001)
            sendWarning('Tracffic light missed !!',
                        "Dear Driver,\n"
                        "This is a reminder from TlSS. "
                        "You have been spotted missing a traffic light. "
                        "Number of times missing the traffic light.\n"
                        "---------------" + str(miss_count) +"---------------\n"
                        "Please understand that if it exceeds 2 times the authorities will be informed.\n"
                        "Please be more careful when you are driving...\n"
                        "thank you",
                        images=[0, 0],
                        email= 'mohamedcoulibaly786@gmail.com')
            print(miss_count)
            if miss_count > 2:
                cv2.imwrite("/Users/mohamedcoulibaly/PycharmProjects/TrafficLightSecuritySystem/ressources/number_plate/"
                            "No_Plate_"+str(shots_count)+".jpg", croppedPlate)
                cv2.imwrite("/Users/mohamedcoulibaly/PycharmProjects/TrafficLightSecuritySystem/ressources/car/"
                            "Car_"+str(shots_count)+".jpg", img)

                images = ["/Users/mohamedcoulibaly/PycharmProjects/TrafficLightSecuritySystem/ressources/number_plate/"
                                "No_Plate_"+str(shots_count)+".jpg",
                                "/Users/mohamedcoulibaly/PycharmProjects/TrafficLightSecuritySystem/ressources/car/"
                                "Car_" + str(shots_count) + ".jpg"
                                ]
                sleep(0.00001)
                sendWarning('Missed traffic Light',
                            "A Driver with this number plate below have been spotted missing few traffic lights.\n"
                            "Number plate attached bellow.\n"
                            "Amount of time missed.\n"
                            "                -------" + str(miss_count) + "-------",
                            images,
                            'mohamedcoulibaly786@gmail.com')
                sleep(0.00001)
                print(miss_count)
                shots_count += 1
            else:
                print("Motion not detected")

        cv2.imshow("live transmission", img)
        key = cv2.waitKey(1)
        if time.time() > timeout_start + timeStop_green:
            OffOnly(green)
        else:
            pass
        if key == ord('s'):
            break

cv2.destroyAllWindows()