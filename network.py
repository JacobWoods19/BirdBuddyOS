import requests

class InternetChecker:
    def __init__(self, url="http://www.example.com"):
        self.url = url

    def check_internet(self):
        try:
            print("Checking internet connection...")
            response = requests.get(self.url, timeout=5)
            # If the request was successful, no exception will be raised.
            response.raise_for_status()
            print("Internet is connected")
        except requests.RequestException:
            print("No internet connection")

if __name__ == "__main__":
    checker = InternetChecker()
    checker.check_internet()