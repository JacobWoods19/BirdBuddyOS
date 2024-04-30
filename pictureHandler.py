from datetime import datetime
import os 
import cv2
from google.cloud import storage
import logging
##Saves Image To Photos Directory With UserID, Date, Time, and handles the max nyumber of images
class PictureHandler:
    def __init__(self,bucket_name, max_images=5):
        self.image_count = 0
        self.bucket_name = bucket_name
    def createDirectory(self, name, path):
        os.mkdir(path + name)
    def validateDirectory(self, name, path):
        return os.path.isdir(path + name)
    def validatePhotosFolder(self):
        return self.validateDirectory("Photos", "./")
    def createPhotosFolder(self):
        if not self.validatePhotosFolder():
            self.createDirectory("Photos", "./")
            print("Photos directory created")
        else:
            print("Photos directory already exists")
    def savePhotoPath(self):
        self.image_count += 1
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H-%M-%S")
        if not self.validateDirectory(current_date, "./Photos/"):
            self.createDirectory(current_date, "./Photos/")
        return "./Photos/" + current_date + "/" + current_time + ".jpg"
    def checkkeyexists(self):
        return os.path.exists("key.json")
    def getAbsPhotoPath(self, date, time):
        return os.path.abspath("./Photos/" + date + "/" + time + ".jpg")
    def getAbsPhotoPath(self, local_path):
        return os.path.abspath(local_path)
    def uploadToGoogleCloudBucket(self, path, destination_blob_name):
        # Remove all handlers associated with the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Configure logging to file only
        logging.basicConfig(
            filename='birdfeeder.log',  # Name of the log file
            filemode='w',              # 'w' to overwrite the file or 'a' to append
            level=logging.DEBUG,       # Logging level
            format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
        )
        # Check if the key file exists
        if not os.path.exists(os.path.abspath("key.json")):
            print("Key does not exist")
            logging.error("Key does not exist")
            return

        if not self.bucket_name:
            print("Bucket name is not set")
            logging.error("Bucket name is not set")
            return
        try:
            storage_client = storage.Client.from_service_account_json(os.path.abspath("key.json"))
            bucket = storage_client.get_bucket(self.bucket_name)

            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(self.getAbsPhotoPath(path))
            
            public_url = f"https://storage.googleapis.com/{self.bucket_name}/{blob.name}"
            print(public_url)
            print(blob.name)

            return public_url
        except Exception as e:
            print(e)
            logging.error(e)
            return None
