import requests

url = "http://127.0.0.1:5000/predict"  # Flask backend URL
files = {'file': open("test_image.png", 'rb')}  # Open an image file
response = requests.post(url, files=files)  # Send image to Flask API
print(response.json())  # Print response (Real/Fake)
