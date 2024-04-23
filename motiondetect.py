import cv2
import numpy as np
import time
class MotionDetector:
    def __init__(self, video_source=0, cool_down_time= 10, sensitivity = 500, debug=False):
        self.cap = cv2.VideoCapture(video_source)
        self.back_sub = cv2.createBackgroundSubtractorMOG2()
        self.debug = debug
        self.cool_down_time = cool_down_time
        self.sensitivity = sensitivity
    def run(self):
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
                print("Capturing image...")
                last_capture = time.time()
                cv2.imwrite("motion_detected.jpg", frame)
                cv2.imwrite("foreground.jpg", fg_mask)
            if self.debug:
                cv2.imshow('Frame', frame)
                cv2.imshow('Foreground', fg_mask)

            if cv2.waitKey(1) == 27:  
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

