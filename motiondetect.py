import cv2
import numpy as np
import time
import requests

from termcolor import colored
class MotionDetector:
    def __init__(self, video_source=0, cool_down_time= 10, sensitivity = 500, pushover = None,  debug=False):
        self.cap = cv2.VideoCapture(video_source)
        self.back_sub = cv2.createBackgroundSubtractorMOG2()
        self.debug = debug
        self.cool_down_time = cool_down_time
        self.sensitivity = sensitivity
        self.pushover = pushover
    def validate_camera_connected(self):
        print("Checking if camera is connected...")
        cameras = self.list_cameras()
        if not cameras:
            print("No cameras found")
            return False
        else:
            print("Camera is connected")
            return True
    def detect_cameras(self):
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

    def select_camera(self):
        cameras = self.list_cameras()
        if cameras:
            print("Select camera:")
            print("----------------")
            for camera in cameras:
                print(camera)
            print("----------------")
        else:
            print("No cameras found")
            return
        while True:
            try:
                selected_index = int(input("Select camera index: "))
                print(f"Selected camera index: {selected_index}")
            except ValueError:
                print("Invalid input")
                continue

            if selected_index not in cameras:
                print("Invalid camera index")
                continue
            else:
                break
        print("Setting video source to: ", selected_index)
        print("Setup complete! Press 'esc' to exit")
        self.video_source = selected_index


    def run(self):
        self.select_camera()
        last_capture = time.time()
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
                self.update_line("Motion Detected", color="green", end_with_newline=False)
                if self.pushover:
                    self.pushover.send_notification(title="BirdBuddy", message="Motion detected at your bird feeder")
                last_capture = time.time()
                cv2.imwrite("motion_detected.jpg", frame)
            elif motion_detected:
                self.update_line("On cool down", color="yellow", end_with_newline=False)
            else:
                self.update_line("No motion detected", color="red", end_with_newline=False)

            if self.debug:
                cv2.imshow('Frame', frame)

            if cv2.waitKey(1) == 27:  
                break

        self.cleanup()
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

