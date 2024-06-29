import torch
import os
import RPi.GPIO as GPIO
from time import sleep, time
import logging
from Uploadimage import upload_image
from bunyiBuzzer import buzzer
from picamera2 import Picamera2
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_camera():
    global picam2
    if picam2 is None:
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
        picam2.configure(camera_config)
        picam2.start()


def setup_button(pin_button):
    GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Set GPIO mode every time after cleanup
 # Setup button pin as input

def activate_solenoid(pin_solenoid, active_duration=1, total_duration=10):
    GPIO.setup(pin_solenoid,GPIO.OUT)
    GPIO.output(pin_solenoid, 1)  # Activate the solenoid
    sleep(active_duration)
    GPIO.output(pin_solenoid, 0)  # Deactivate solenoid
    sleep(total_duration - active_duration)

def detect_objects_in_file(weights, folder_path, img_size=640, conf_thresh=0.25, solenoid_pin=14):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)
    filename = next((f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')), None)
    
    if filename:
        image_path = os.path.join(folder_path, filename)
        results = model(image_path, size=img_size)
        file_name, _ = os.path.splitext(filename)
        logging.info(f"Predictions for {filename}")
        for pred in results.pred:
            classes = pred[:, -1]
            confidences = pred[:, 4]
            for class_index, confidence_score in zip(classes, confidences):
                if class_index.item() == 1 and confidence_score.item() > 0.78:
                    logging.info(f"Class: {class_index.item()} - Confidence: {confidence_score.item()}")
                    setup_gpio()
                    activate_solenoid(solenoid_pin)
                    GPIO.cleanup()
                    upload_image(file_name, status='verified')
                    return
                else:
                    upload_image(file_name, status='unverified')
                    #buzzer()
                    return
        logging.info("-----------------------------------")
    else:
        logging.warning("No image files found in the folder.")

if __name__ == "__main__":
    try:
        global picam2
        picam2 = None
        initialize_camera()
        setup_gpio()
        setup_button(26)
        while True:
            print("Waiting for button press to capture image...")
            GPIO.wait_for_edge(26, GPIO.FALLING)
            print("Button pressed! Capturing image...")
            sleep(3)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./foto_sementara/image_{timestamp}.jpg"
            picam2.capture_file(filename)
            print(f"Image saved as {filename}")
            detect_objects_in_file(
                weights='./best_4Orang.pt',
                folder_path='./foto_sementara'
            )
            sleep(1)
            setup_gpio()
            setup_button(26)
    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")
    finally:
        if picam2:
            picam2.stop()
        GPIO.cleanup()
