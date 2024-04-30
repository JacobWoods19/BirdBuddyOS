import requests 
import datetime
import uuid
import logging
class NetworkManager:
    """
    Manages network operations such as checking internet connectivity and uploading images to a server.

    Attributes:
        url (str): The URL used for checking internet connectivity.

    Parameters:
        url (str): Optional; default URL for internet connectivity checks. Default is "http://www.example.com".
    """
    def __init__(self, url="http://www.example.com"):
        self.url = url
    def check_internet(self):
        """
        Checks if the internet connection is available by making a GET request to the specified URL.

        Uses a timeout to limit how long the request waits for a response. Prints the connection status.
        """
        try:
            print("Checking internet connection...")
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            print("Internet is connected")
        except requests.RequestException:
            print("No internet connection")
    def upload_image(self, user_id, file_location, image_name):
        """
        Uploads an image's data to a server using a POST request.

        Parameters:
            user_id (str): The identifier for the user.
            file_location (str): The URL where the image is stored.
            image_name (str): The name of the image file.

        The method prints details about the process and the server's response. It also handles and prints
        different HTTP errors based on the server's response status.
        """
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
        try:
            current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            headers = {
            "Content-Type": "application/json",
            }
        # JSON Payload
            json_body = {
                "USER_ID": "test",
                "GCS_OBJECT_URL": file_location,
                "DATE_TIME": current_date_time,
                "IMAGE_LOCATION": "Test Bird House",
                "IMAGE_NAME": image_name
            }
            print(json_body)
            response = requests.post("https://clippyserver.uc.r.appspot.com/api/insert/test", json=json_body, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print(response_json)
        except Exception as e:
            if response.status_code == 404:
                logging.error("Server not found")
            elif response.status_code == 500:
                logging.error("Server error")
                print(response.text)
            elif response.status_code == 422:
                logging.error("No bird found")
            elif response.status_code == 200 or response.status_code == 422:
                logging.info("Bird found")
            else:
                print("An error occurred")
                print(e)   
# if __name__ == "__main__":
#     checker = NetworkManager()
#     checker.check_internet()
#     destination_blob_name = "1001.jpg"
#     print(destination_blob_name)
#     checker.upload_image("test", "https://console.cloud.google.com/clippy_bird-2", destination_blob_name)
