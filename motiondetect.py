import cv2
import numpy as np
import time
import requests
from pushover import PushoverHandler
from pictureHandler import PictureHandler
from termcolor import colored
import uuid 
import logging
import threading
    # A class to handle motion detection from video sources, with options for debugging,
    # cloud backup, and notifications.

    # Attributes:
    #     cap (cv2.VideoCapture): Video capture object for the specified video source.
    #     back_sub (cv2.BackgroundSubtractorMOG2): Background subtractor object for motion detection.
    #     debug (bool): Flag to enable debugging outputs.
    #     is_cloud_backup_enabled (bool): Status of cloud backup functionality.
    #     cool_down_time (int): Minimum time between motion detections to avoid false alarms.
    #     sensitivity (int): Threshold for motion detection sensitivity.
    #     pushover (PushoverHandler): Handler for sending notifications via Pushover.
    #     picture_handler (PictureHandler): Handler for processing and saving pictures.
    #     network_handler (NetworkHandler): Handler for network-related operations.
    #     backup_enabled (bool): Flag to enable backup functionality.
    #     user_id (str): User identifier for tracking or user-specific operations.

    # Parameters:
    #     picture_handler (PictureHandler): An instance of a handler for picture operations.
    #     network_handler (NetworkHandler): An instance of a handler for network operations.
    #     user_id (str): Identifier of the user.
    #     backup_enabled (bool): Enables backup of captured images to cloud storage. Default is True.
    #     video_source (int): Device index of the video source. Default is 0.
    #     cool_down_time (int): Cool-down time between detections in seconds. Default is 10.
    #     sensitivity (int): Sensitivity threshold for detecting motion. Default is 500.
    #     pushover (PushoverHandler): Optional handler for Pushover notifications. Default is None.
    #     debug (bool): Enables debug mode. Default is False.
class MotionDetector:

    def __init__(self,picture_handler,network_handler,user_id, backup_enabled=True , video_source=0, cool_down_time= 10, sensitivity = 500, pushover = None,  debug=False):
        self.cap = cv2.VideoCapture(video_source)
        self.back_sub = cv2.createBackgroundSubtractorMOG2()
        self.debug = debug
        self.is_cloud_backup_enabled = False
        self.cool_down_time = cool_down_time
        self.sensitivity = sensitivity
        self.pushover = pushover
        self.picture_handler = picture_handler
        self.network_handler = network_handler
        self.backup_enabled = backup_enabled
        self.user_id = user_id

        
    def detect_cameras(self):
        """
        Detects and lists available video capture devices.

        Returns:
            list: Indexes of available video capture devices.
        """ 
                
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_V4L2)  # Use CAP_V4L2 for direct V4L2 access
            if not cap.isOpened():
                cap.release()
                break
            else:
                is_open, frame = cap.read()
                if is_open:
                    print(f"Webcam detected at index {index}")
                    arr.append(index)
                cap.release()
            index += 1
        return arr



    def run(self):
        """
        Runs the motion detection loop. This method handles the capturing and processing of video frames,
        detects motion, and performs actions based on the motion detection results.
        """
        last_capture = time.time()
        # Configure logging to file only
        logging.basicConfig(
            filename='birdfeeder.log',  # Name of the log file
            filemode='w',              # 'w' to overwrite the file or 'a' to append
            level=logging.DEBUG,       # Logging level
            format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
        )
        while True:

            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fg_mask = self.back_sub.apply(gray)

            kernel = np.ones((5,5), np.uint8)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > self.sensitivity:
                    motion_detected = True
                    if self.debug:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    break

            time_elapsed = time.time() - last_capture
            if motion_detected and time_elapsed > self.cool_down_time:
                # self.update_line("Motion Detected", color="green", end_with_newline=False)
                logging.info("Motion detected at the bird feeder")

                if self.pushover:
                    logging.info("Sending notification to Pushover")
                    self.pushover.send_notification(title="BirdBuddy", message="Motion detected at your bird feeder")
                last_capture = time.time()
                ##Where the photo will be saved
                path = self.picture_handler.savePhotoPath()
                cv2.imwrite(path, frame)
                if self.backup_enabled:
                    destination_blob_name = uuid.uuid4().hex + ".jpg"
                    x = threading.Thread(target=self.upload_image, args=(path, destination_blob_name))
                    x.start()
                    

            elif motion_detected:
                self.update_line("On cool down", color="yellow", end_with_newline=False)
            else:
                self.update_line("No motion detected", color="red", end_with_newline=False)

            if self.debug:
                cv2.imshow('Frame', frame)

            if cv2.waitKey(1) == 27:  
                break
        self.cleanup()
    def upload_image(self, path, destination_blob_name):
        public_url = self.picture_handler.uploadToGoogleCloudBucket(path=path, destination_blob_name=destination_blob_name)
        self.network_handler.upload_image(user_id=self.user_id, file_location=public_url, image_name=destination_blob_name)
    def update_line(self, message,color, width=80, end_with_newline=True):
        # Ensure the message fills the entire width or is truncated to fit it
        padded_message = message.ljust(width)[:width]
        # Print the message with a carriage return and flush the output
        print(colored(padded_message, color), end='\r', flush=True)
        
        # Optionally end with a newline when the updates are complete
        if end_with_newline:
            print()  # Print the newline character at the end

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

